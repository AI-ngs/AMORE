"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

const MOCK_TREND_DATA = [
  { date: "Week 1", rank: 8 },
  { date: "Week 2", rank: 6 },
  { date: "Week 3", rank: 4 },
  { date: "Week 4", rank: 5 },
  { date: "Week 5", rank: 3 },
  { date: "Week 6", rank: 2 },
  { date: "Week 7", rank: 3 },
]

export function TrendChart() {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={MOCK_TREND_DATA}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis dataKey="date" stroke="#9ca3af" />
        <YAxis reversed stroke="#9ca3af" />
        <Tooltip />
        <Line type="monotone" dataKey="rank" stroke="#0ea5e9" strokeWidth={2} dot={{ fill: "#0ea5e9", r: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  )
}
