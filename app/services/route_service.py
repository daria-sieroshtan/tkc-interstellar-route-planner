import heapq
from dataclasses import dataclass

from app.repositories.gate_repository import GateRepository
from app.schemas.gate import RouteResponse, RouteSegment


@dataclass
class Edge:
    to_vertex: str
    weight: float


@dataclass
class VertexPathInfo:
    vertex_id: str
    distance: float
    predecessor: str | None


@dataclass
class ShortestPathResult:
    vertex_paths: list[VertexPathInfo]

    def get_distance(self, vertex_id: str) -> float | None:
        for vertex in self.vertex_paths:
            if vertex.vertex_id == vertex_id:
                return vertex.distance
        return None

    def get_predecessor(self, vertex_id: str) -> str | None:
        for vertex in self.vertex_paths:
            if vertex.vertex_id == vertex_id:
                return vertex.predecessor
        return None


class RouteService:
    COST_PER_PASSENGER_PER_HU = 0.10

    def __init__(self, gate_repository: GateRepository):
        self.gate_repository = gate_repository

    async def calculate_cheapest_route(self, start_gate_id: str, end_gate_id: str) -> RouteResponse | None:
        start_gate_id = start_gate_id.upper()
        end_gate_id = end_gate_id.upper()

        start_exists = await self.gate_repository.gate_exists(start_gate_id)
        end_exists = await self.gate_repository.gate_exists(end_gate_id)

        if not start_exists or not end_exists:
            return None

        # Production optimization: cache the graph structure and route results to avoid
        # repeated DB queries and pathfinding calculations (not implemented for demo)
        all_connections = await self.gate_repository.get_all_connections()

        graph = self._build_graph(all_connections)

        result = self._dijkstra(graph, start_gate_id, end_gate_id)

        end_distance = result.get_distance(end_gate_id)
        if end_distance is None or end_distance == float("inf"):
            return None

        path = self._reconstruct_path(result, start_gate_id, end_gate_id, graph)

        total_distance_hu = end_distance
        total_cost = total_distance_hu * self.COST_PER_PASSENGER_PER_HU

        return RouteResponse(
            start_gate_id=start_gate_id,
            end_gate_id=end_gate_id,
            total_distance_hu=total_distance_hu,
            total_cost=total_cost,
            path=path,
        )

    def _build_graph(self, connections: list[RouteSegment]) -> dict[str, list[Edge]]:
        graph: dict[str, list[Edge]] = {}
        for connection in connections:
            if connection.from_gate_id not in graph:
                graph[connection.from_gate_id] = []
            graph[connection.from_gate_id].append(Edge(to_vertex=connection.to_gate_id, weight=connection.distance_hu))
        return graph

    def _dijkstra(self, graph: dict[str, list[Edge]], start: str, end: str) -> ShortestPathResult:
        distances = {start: 0.0}
        predecessors = {}

        # Priority queue: (distance, gate_id)
        pq = [(0.0, start)]
        visited = set()

        while pq:
            current_distance, current_gate = heapq.heappop(pq)

            if current_gate in visited:
                continue

            visited.add(current_gate)

            if current_gate == end:
                break

            if current_distance > distances.get(current_gate, float("inf")):
                continue

            for edge in graph.get(current_gate, []):
                distance = current_distance + edge.weight

                if distance < distances.get(edge.to_vertex, float("inf")):
                    distances[edge.to_vertex] = distance
                    predecessors[edge.to_vertex] = current_gate
                    heapq.heappush(pq, (distance, edge.to_vertex))

        vertex_paths = [
            VertexPathInfo(
                vertex_id=vertex_id,
                distance=distances[vertex_id],
                predecessor=predecessors.get(vertex_id),
            )
            for vertex_id in distances
        ]
        return ShortestPathResult(vertex_paths=vertex_paths)

    def _reconstruct_path(
        self, result: ShortestPathResult, start: str, end: str, graph: dict[str, list[Edge]]
    ) -> list[RouteSegment]:
        path = []
        current = end

        while current != start:
            prev = result.get_predecessor(current)
            if prev is None:
                return []

            distance = None
            for edge in graph.get(prev, []):
                if edge.to_vertex == current:
                    distance = edge.weight
                    break

            if distance is not None:
                path.append(RouteSegment(from_gate_id=prev, to_gate_id=current, distance_hu=distance))

            current = prev

        path.reverse()
        return path
