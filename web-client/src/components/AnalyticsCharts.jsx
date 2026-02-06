import React from 'react';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { Radar, Scatter } from 'react-chartjs-2';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

const AnalyticsCharts = ({ equipmentList }) => {
  if (!equipmentList) return null;

  // Prepare Scatter Data: Flowrate vs Pressure
  // Limit to 100 points for performance if dataset is huge
  const scatterData = {
    datasets: [
      {
        label: 'Flow vs Pressure Correlation',
        data: equipmentList.slice(0, 100).map(item => ({
          x: item.flowrate,
          y: item.pressure,
        })),
        backgroundColor: 'rgba(59, 130, 246, 0.6)', 
      },
    ],
  };

  const scatterOptions = {
    responsive: true,
    scales: {
      x: { title: { display: true, text: 'Flowrate (m³/h)' } },
      y: { title: { display: true, text: 'Pressure (bar)' } },
    },
    plugins: { legend: { position: 'top' } }
  };

  // Prepare Radar Data: Average Metrics by Type
  // We need to aggregate data manually here
  const types = [...new Set(equipmentList.map(e => e.type))];
  const radarDatasets = types.map((type, i) => {
      const items = equipmentList.filter(e => e.type === type);
      const avgFlow = items.reduce((acc, curr) => acc + curr.flowrate, 0) / items.length;
      const avgPress = items.reduce((acc, curr) => acc + curr.pressure, 0) / items.length;
      const avgTemp = items.reduce((acc, curr) => acc + curr.temperature, 0) / items.length;
      
      // Normalize slightly for visualization if scales are wildly different
      // For this demo, we plot raw values assuming they are somewhat comparable orders of magnitude
      
      const colors = ['rgba(59, 130, 246, 0.2)', 'rgba(239, 68, 68, 0.2)', 'rgba(16, 185, 129, 0.2)'];
      const borderColors = ['#3b82f6', '#ef4444', '#10b981'];
      
      return {
          label: type,
          data: [avgFlow, avgPress, avgTemp],
          backgroundColor: colors[i % 3],
          borderColor: borderColors[i % 3],
          borderWidth: 2,
      };
  });

  const radarData = {
      labels: ['Avg Flowrate', 'Avg Pressure', 'Avg Temperature'],
      datasets: radarDatasets.slice(0, 3) // Limit to top 3 types to avoid clutter
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Scatter Chart */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-800 mb-4">Correlation Analysis</h3>
        <div className="h-80">
            <Scatter data={scatterData} options={scatterOptions} />
        </div>
      </div>

      {/* Radar Chart */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-semibold text-slate-800 mb-4">Type Comparison (Averages)</h3>
        <div className="h-80 flex justify-center">
            <Radar data={radarData} />
        </div>
      </div>
    </div>
  );
};

export default AnalyticsCharts;