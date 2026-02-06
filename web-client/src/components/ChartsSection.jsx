import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const ChartsSection = ({ distribution, equipmentList }) => {
  if (!distribution || !equipmentList) return null;

  // Prepare Data for Doughnut Chart 
  const pieData = {
    labels: distribution.map(d => d.type),
    datasets: [
      {
        data: distribution.map(d => d.count),
        backgroundColor: [
          '#3b82f6', // blue-500
          '#ef4444', // red-500
          '#10b981', // emerald-500
          '#f59e0b', // amber-500
          '#8b5cf6', // violet-500
          '#ec4899', // pink-500
        ],
        borderWidth: 0,
      },
    ],
  };

  // Prepare Data for Bar Chart (Top 5 Highest Pressure Equipment)
  // Sorting to show the most critical equipment
  const sortedByPressure = [...equipmentList].sort((a, b) => b.pressure - a.pressure).slice(0, 5);
  
  const barData = {
    labels: sortedByPressure.map(d => d.name),
    datasets: [
      {
        label: 'Pressure (bar)',
        data: sortedByPressure.map(d => d.pressure),
        backgroundColor: '#6366f1',
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' },
    },
    maintainAspectRatio: false,
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      {/* Distribution Chart */}
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Equipment Type Distribution</h3>
        <div className="h-64 flex justify-center">
            <Doughnut data={pieData} options={options} />
        </div>
      </div>

      {/* Pressure Chart */}
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Critical Pressure Levels (Top 5)</h3>
        <div className="h-64">
            <Bar data={barData} options={options} />
        </div>
      </div>
    </div>
  );
};

export default ChartsSection;