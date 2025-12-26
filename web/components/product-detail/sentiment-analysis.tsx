"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts"

const SENTIMENT_DATA = [
  { name: "Positive", value: 68, color: "#10b981" },
  { name: "Neutral", value: 22, color: "#94a3b8" },
  { name: "Negative", value: 10, color: "#ef4444" },
]

export function SentimentAnalysis() {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie data={SENTIMENT_DATA} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={2} dataKey="value">
          {SENTIMENT_DATA.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  )
}
