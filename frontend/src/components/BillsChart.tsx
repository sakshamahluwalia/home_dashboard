// src/components/BillsChart.tsx
import React from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LabelList, // Import LabelList
} from "recharts";
import { Bill } from "../services/billsService";

interface BillsChartProps {
  bills: Bill[];
  chartType: "line" | "bar";
}

interface ChartDataPoint {
  month: number;
  [key: string]: number | string;
}

const getColor = (index: number): string => {
  const colors = [
    "#8884d8",
    "#82ca9d",
    "#ffc658",
    "#ff7300",
    "#a4de6c",
    "#d0ed57",
    "#8dd1e1",
    "#83a6ed",
    "#8e4585",
    "#ff7f50",
    "#87cefa",
    "#da70d6",
  ];
  return colors[index % colors.length];
};

const BillsChart: React.FC<BillsChartProps> = ({ bills, chartType }) => {
  const serviceProviders = Array.from(
    new Set(bills.map((bill) => bill.service_provider))
  );

  // Extract months from filtered bills data
  const months = Array.from(new Set(bills.map((bill) => bill.month))).sort(
    (a, b) => a - b
  );

  const chartData: ChartDataPoint[] = months.map((month) => {
    const dataPoint: ChartDataPoint = { month };
    serviceProviders.forEach((provider) => {
      const bill = bills.find(
        (b) => b.month === month && b.service_provider === provider
      );
      dataPoint[provider] = bill ? bill.amount : 0;
    });
    return dataPoint;
  });

  const ChartComponent = chartType === "line" ? LineChart : BarChart;

  const RenderedComponents = serviceProviders.map((provider, index) => {
    const color = getColor(index);
    if (chartType === "line") {
      return (
        <Line
          key={provider}
          type="monotone"
          dataKey={provider}
          stroke={color}
          activeDot={{ r: 8 }}
        />
      );
    } else {
      return (
        <Bar key={provider} dataKey={provider} stackId="a" fill={color}>
          <LabelList dataKey={provider} position="center" fill="black" />
        </Bar>
      );
    }
  });

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ChartComponent
        data={chartData}
        margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="month"
          tickFormatter={(tick) =>
            new Date(0, tick - 1).toLocaleString("default", { month: "short" })
          }
        />
        <YAxis />
        <Tooltip />
        <Legend />
        {RenderedComponents}
      </ChartComponent>
    </ResponsiveContainer>
  );
};

export default BillsChart;
