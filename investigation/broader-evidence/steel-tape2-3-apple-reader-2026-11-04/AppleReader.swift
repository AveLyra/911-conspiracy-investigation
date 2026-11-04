import Foundation
import AVFoundation
import CoreMedia
import CoreVideo
import Darwin

func rawTime(_ t: CMTime) -> [Any] { [t.value, t.timescale, t.flags.rawValue, t.epoch] }
func fourCC(_ n: FourCharCode) -> String {
    let b = [UInt8((n >> 24) & 255), UInt8((n >> 16) & 255), UInt8((n >> 8) & 255), UInt8(n & 255)]
    return String(bytes: b, encoding: .ascii) ?? String(format: "0x%08x", n)
}
func errorInfo(_ error: Error) -> [String: Any] {
    let e = error as NSError
    return ["domain": e.domain, "code": e.code, "description": e.localizedDescription,
            "failure_reason": e.localizedFailureReason ?? NSNull() as Any]
}
func statusName(_ s: AVAssetReader.Status) -> String {
    switch s { case .unknown: return "unknown"; case .reading: return "reading"
    case .completed: return "completed"; case .failed: return "failed"
    case .cancelled: return "cancelled"; @unknown default: return "unrecognized" }
}

@main struct Main {
    static func main() async {
        guard CommandLine.arguments.count == 4 else {
            fputs("Usage: AppleReader SOURCE nil|argb NEW_JSON\n", stderr); exit(2)
        }
        let source = URL(fileURLWithPath: CommandLine.arguments[1])
        let mode = CommandLine.arguments[2]
        let destination = URL(fileURLWithPath: CommandLine.arguments[3])
        guard ["nil", "argb"].contains(mode) else { exit(2) }
        var result: [String: Any] = ["started_utc": ISO8601DateFormatter().string(from: Date()),
            "mode": mode, "requested_output": mode == "nil" ? "nil storage-format settings" : "kCVPixelFormatType_32ARGB",
            "default_time_range_untouched": true, "counts_complete": false,
            "audio_requested": false, "media_output_written": false,
            "buffer_limit": 20000, "sample_row_schema": ["buffer_index", "num_samples", "pts", "dts", "duration", "total_sample_size", "format_fourcc", "has_image_buffer", "do_not_display_attachment_or_null"],
            "raw_time_schema": ["value", "timescale", "flags", "epoch"]]
        do {
            let asset = AVURLAsset(url: source)
            result["stage"] = "loading_video_tracks"
            let tracks = try await asset.loadTracks(withMediaType: .video)
            result["video_track_count"] = tracks.count
            if let duration = try? await asset.load(.duration) { result["asset_duration"] = rawTime(duration) }
            guard let track = tracks.first else {
                result["stage"] = "no_video_tracks"
                try write(result, to: destination); return
            }
            if let range = try? await track.load(.timeRange) {
                result["track_time_range_start"] = rawTime(range.start)
                result["track_time_range_duration"] = rawTime(range.duration)
            }
            if let descriptions = try? await track.load(.formatDescriptions) {
                result["track_format_fourccs"] = descriptions.map { fourCC(CMFormatDescriptionGetMediaSubType($0)) }
            }
            result["stage"] = "creating_reader"
            let reader = try AVAssetReader(asset: asset)
            let settings: [String: Any]? = mode == "nil" ? nil : [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB]
            let output = AVAssetReaderTrackOutput(track: track, outputSettings: settings)
            output.alwaysCopiesSampleData = false
            result["can_add_output"] = reader.canAdd(output)
            guard reader.canAdd(output) else {
                result["stage"] = "cannot_add_output"
                try write(result, to: destination); return
            }
            reader.add(output)
            result["reader_default_time_range_start"] = rawTime(reader.timeRange.start)
            result["reader_default_time_range_duration"] = rawTime(reader.timeRange.duration)
            result["start_reading_return"] = reader.startReading()
            var rows: [[Any]] = []
            var samples = 0
            var imageBuffers = 0
            var zeroSampleBuffers = 0
            var formats: [String: Int] = [:]
            var limitReached = false
            result["stage"] = "reading"
            while let buffer = output.copyNextSampleBuffer() {
                let count = CMSampleBufferGetNumSamples(buffer)
                let image = CMSampleBufferGetImageBuffer(buffer) != nil
                let description = CMSampleBufferGetFormatDescription(buffer)
                let format = description.map { fourCC(CMFormatDescriptionGetMediaSubType($0)) } ?? "none"
                let attachments = CMSampleBufferGetSampleAttachmentsArray(buffer, createIfNecessary: false) as? [NSDictionary]
                let doNotDisplay: Any = attachments?.first?.object(forKey: kCMSampleAttachmentKey_DoNotDisplay) ?? NSNull()
                rows.append([rows.count, count, rawTime(CMSampleBufferGetPresentationTimeStamp(buffer)),
                             rawTime(CMSampleBufferGetDecodeTimeStamp(buffer)), rawTime(CMSampleBufferGetDuration(buffer)),
                             CMSampleBufferGetTotalSampleSize(buffer), format, image, doNotDisplay])
                samples += count
                if image { imageBuffers += 1 }
                if count == 0 { zeroSampleBuffers += 1 }
                formats[format, default: 0] += 1
                if rows.count >= 20000 { reader.cancelReading(); limitReached = true; break }
            }
            result["reader_status"] = statusName(reader.status)
            result["reader_status_raw"] = reader.status.rawValue
            result["counts_complete"] = reader.status == .completed && !limitReached
            result["buffer_count"] = rows.count
            result["sample_count_sum"] = samples
            result["image_buffer_count"] = imageBuffers
            result["zero_sample_buffer_count"] = zeroSampleBuffers
            result["observed_buffer_formats"] = formats
            result["sample_rows"] = rows
            result["buffer_limit_reached"] = limitReached
            if let error = reader.error { result["reader_error"] = errorInfo(error) }
            result["stage"] = "reader_terminal"
        } catch {
            result["caught_error"] = errorInfo(error)
        }
        do { try write(result, to: destination) }
        catch { fputs("Result write failed: \(error)\n", stderr); exit(3) }
    }
    static func write(_ original: [String: Any], to url: URL) throws {
        var value = original
        value["finished_utc"] = ISO8601DateFormatter().string(from: Date())
        var data = try JSONSerialization.data(withJSONObject: value, options: [.sortedKeys])
        data.append(10)
        guard data.count < 16 * 1024 * 1024 else {
            throw NSError(domain: "BoundedReaderOutput", code: 1, userInfo: [NSLocalizedDescriptionKey: "Metadata exceeds local size cap; route a new output through verified media store"])
        }
        try data.write(to: url, options: .withoutOverwriting)
        print("Recorded \(value["stage"] ?? "unknown") counts_complete=\(value["counts_complete"] ?? false)")
    }
}
