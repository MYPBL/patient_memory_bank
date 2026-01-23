import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

export function MedicalGraph({ patientId }: { patientId: string }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [data, setData] = useState({ nodes: [], edges: [] });

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const res = await fetch(`http://localhost:5000/api/graph?patientId=${patientId}`);
        const graph = await res.json();
        setData(graph);
      } catch (err) {
        console.error("Failed to fetch graph:", err);
      }
    };
    fetchGraph();
    const interval = setInterval(fetchGraph, 5000); 
    return () => clearInterval(interval);
  }, [patientId]);

  useEffect(() => {
    if (!svgRef.current || data.nodes.length === 0) return;
    
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;
    const g = svg.append("g");

    // --- CRITICAL FIX: Map 'from/to' to 'source/target' ---
    const formattedNodes = data.nodes.map((d: any) => ({ ...d }));
    const formattedLinks = data.edges.map((d: any) => ({
      ...d,
      source: d.from, // D3 needs 'source'
      target: d.to    // D3 needs 'target'
    }));

    const simulation = d3.forceSimulation(formattedNodes as any)
      .force("link", d3.forceLink(formattedLinks).id((d: any) => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = g.append("g")
      .selectAll("line")
      .data(formattedLinks)
      .join("line")
      .attr("stroke", "#cbd5e1")
      .attr("stroke-width", 2);

    const node = g.append("g")
      .selectAll("g")
      .data(formattedNodes)
      .join("g");

    node.append("circle")
      .attr("r", (d: any) => d.node_type === "concept" ? 12 : 8)
      .attr("fill", (d: any) => d.node_type === "concept" ? "#2563eb" : "#dc2626");

    node.append("text")
      .text((d: any) => d.name)
      .attr("x", 15).attr("y", 5)
      .style("font-size", "12px").style("font-weight", "500");

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });
  }, [data]);

  return (
    <div style={{ height: '100%', border: '1px solid #e2e8f0', borderRadius: '8px', backgroundColor: 'white', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '12px', borderBottom: '1px solid #f1f5f9', background: '#f8fafc', fontSize: '14px', fontWeight: 'bold', color: '#475569' }}>
        SHARED COGNITIVE MEMORY GRAPH
      </div>
      <svg ref={svgRef} style={{ flex: 1, width: '100%' }} />
    </div>
  );
}