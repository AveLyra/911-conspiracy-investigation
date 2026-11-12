#!/usr/bin/env python3
"""Reproduce the stated idealized Korol balance; not a physical collapse simulation."""
import math

g = 9.81
area = 3853.0
height = 3.89
normal_floor_mass = (3.6 + 0.5 * 2.4) * 1000 * area / g
heavy_floor_mass = (4.3 + 0.5 * 3.6) * 1000 * area / g
block_mass = 32 * normal_floor_mass + 3 * heavy_floor_mass + 6_530_000

def column_work(n, multiplier=3.5):
    return n * 0.9 * math.pi * 10.7e6 * 276 * multiplier / 1000

first_speed = math.sqrt(2 * (block_mass * g * height - column_work(27)) / block_mass)
post_first_impact = block_mass / (block_mass + normal_floor_mass) * first_speed
second_mass = block_mass + normal_floor_mass
second_speed = math.sqrt(post_first_impact**2 + 2*g*height - 2*column_work(27)/second_mass)
third_mass = block_mass + 2 * normal_floor_mass
post_second_impact = second_mass / third_mass * second_speed
available = 0.5 * third_mass * post_second_impact**2 + third_mass*g*height
slab_work = 4900 * area * 0.1016 * 2400
print(f'floor masses kg: {normal_floor_mass:.3f}, {heavy_floor_mass:.3f}')
print(f'upper block kg: {block_mass:.3f}')
print(f'first / post-first / second / post-second speed m/s: {first_speed:.6f}, {post_first_impact:.6f}, {second_speed:.6f}, {post_second_impact:.6f}')
print(f'available / columns / slab GJ: {available/1e9:.6f}, {column_work(82)/1e9:.6f}, {slab_work/1e9:.6f}')
for fraction in (1.0, 0.99, 0.95):
    residual = available - column_work(82) - fraction*slab_work
    result = f'{math.sqrt(2*residual/third_mass):.3f} m/s' if residual > 0 else 'non-positive energy balance'
    print(f'slab fraction {fraction:.2f}: residual {residual/1e9:+.6f} GJ; {result}')
print(f'five slabs, 101.6 mm GJ: {5*slab_work/1e9:.6f}')
print(f'thickness needed for 32.01 GJ mm: {32.01e9/(5*4900*area*2400)*1000:.3f}')
