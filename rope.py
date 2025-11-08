from __future__ import annotations

import dataclasses
import math

@dataclasses.dataclass
class Vector:
    x: int = 0.0
    y: int = 0.0
    
    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"
    
    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)
    
    def __add__(self, addend: Vector) -> Vector:
        return Vector(self.x + addend.x, self.y + addend.y)
        
    def __sub__(self, subtrahend: Vector) -> Vector:
        return Vector(self.x - subtrahend.x, self.y - subtrahend.y)
    
    def __mul__(self, factor: float) -> Vector:
        return Vector(self.x * factor, self.y * factor)
    
    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def unit_vector(self) -> Vector:
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)
    
    def distance(self, other: Vector) -> float:
        return (self - other).magnitude()
    
    def direction_to(self, other: Vector) -> Vector:
        return (other - self).unit_vector()
    
    def middle(self, other: Vector) -> Vector:
        return (self + other) * 0.5
    

class Circle:
    __slots__ = ('center', 'radius')
    
    def __init__(self, center: Vector, radius: int = 100) -> None:
        self.center = center
        self.radius = radius
        
    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius})"
    
    def is_inside(self, position: Vector) -> bool:
        if position.distance(self.center) < self.radius:
            return True
        return False
        
    def resolve_collision(self, position: Vector) -> Vector:
        difference = position - self.center
        distance = position.distance(self.center)
        normal = Vector()
        
        if distance == 0:
            normal.x = 1
            distance = 0.0001
        else:
            normal = difference * (1 / distance)
        
        penetration = self.radius - distance
        resolved_position = position + normal * penetration
        
        return resolved_position
    

class Rectangle:
    __slots__ = ('center', 'size')
    
    def __init__(self, center: Vector, size: Vector) -> None:
        self.center = center
        self.size = size
        
    def __repr__(self) -> str:
        return f"Rectangle(center={self.center}, size={self.size})"
    
    def is_inside(self, position: Vector) -> bool:
        if self.center.x + self.size.x / 2 > position.x > self.center.x - self.size.x / 2:
            if self.center.y + self.size.y / 2 > position.y > self.center.y - self.size.y / 2:
                return True
        return False
        
    def resolve_collision(self, position: Vector) -> Vector:
        left_overlap   = (self.center.x - self.size.x / 2) - position.x
        right_overlap  = (self.center.x + self.size.x / 2) - position.x
        bottom_overlap = (self.center.y - self.size.y / 2) - position.y
        top_overlap    = (self.center.y + self.size.y / 2) - position.y
        
        minimum_x = left_overlap if abs(left_overlap) < abs(right_overlap) else right_overlap
        minimum_y = bottom_overlap if abs(bottom_overlap) < abs(top_overlap) else top_overlap
        
        resolved_position = position
        if abs(minimum_x) < abs(minimum_y):
            resolved_position.x += minimum_x
        else:
            resolved_position.y += minimum_y
            
        return resolved_position


class Node:
    def __init__(self, mass: float = 0.0, position: Vector = Vector(), fixed: bool = False) -> None:
        self.mass     = mass
        self.position = position
        self.fixed    = fixed

        self.previous_position = position
    
    def __repr__(self) -> str:
        return f"Node(mass={self.mass}, position={self.position}, fixed={self.fixed})"


class Rope:
    def __init__(self, node_count: int, mass: float, start_position: Vector, end_position: Vector) -> None:
        self.segment_length: int = start_position.distance(end_position) / node_count
        self.nodes: list[Node] = []
        direction = start_position.direction_to(end_position)
        for i in range(node_count):
            self.nodes.append(Node(mass / node_count, start_position + direction * i * self.segment_length))
            
        # by default, set the first and last nodes to be fixed
        self.nodes[0].fixed  = True
        self.nodes[-1].fixed = True

    def __repr__(self) -> str:
        return f"Rope(segment_length={self.segment_length}, nodes={self.nodes})"
    
    def update(self, gravity: Vector, delta_time: float, simulation_iterations: int = 20, environment: list[Circle | Rectangle] = []) -> None:
        for node in self.nodes:
            if not node.fixed:
                previous_position = node.position
                velocity = node.position - node.previous_position
                node.position += velocity + gravity * (delta_time ** 2)
                node.previous_position = previous_position
        
        # more simulation iterations will increase the accuracy of the node length fixing
        # however it will also reduce performance
        for _ in range(simulation_iterations):
            for i in range(len(self.nodes) - 1):
                current_node = self.nodes[i]
                next_node    = self.nodes[i + 1]
                
                distance = current_node.position.distance(next_node.position)
                if distance >= self.segment_length:
                    direction = current_node.position.direction_to(next_node.position)
                    middle    = current_node.position.middle(next_node.position)
                    
                    if not current_node.fixed:
                        current_node.position = middle - direction * self.segment_length * 0.5
                    if not next_node.fixed:
                        next_node.position = middle + direction * self.segment_length * 0.5
                        
            for object in environment:
                for node in self.nodes:
                    if object.is_inside(node.position):
                        node.position = object.resolve_collision(node.position)
