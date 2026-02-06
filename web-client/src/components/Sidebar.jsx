import React from 'react';
import { LayoutDashboard, PieChart, Database } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'analytics', label: 'Analytics', icon: PieChart },
    { id: 'data', label: 'Data Logs', icon: Database },
  ];

  return (
    <div className="w-64 bg-slate-900 h-screen fixed left-0 top-0 flex flex-col text-white shadow-xl z-50">
      {/* App Title */}
      <div className="h-16 flex items-center px-4 border-b border-slate-800">
        <div className="w-8 h-8 bg-blue-700 rounded-lg flex items-center justify-center mr-3 font-bold text-xs">
          CEV
        </div>
        <span className="font-semibold text-sm leading-tight">
          Chemical Equipment<br/>Visualizer
        </span>
      </div>

      {/* Navigation Menu */}
      <nav className="flex-1 py-6 px-3 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group ${
                isActive 
                  ? 'bg-blue-700 text-white shadow-md' 
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <Icon size={20} className={isActive ? 'text-white' : 'text-slate-400 group-hover:text-white'} />
              <span className="font-medium text-sm">{item.label}</span>
            </button>
          );
        })}
      </nav>
      
      {/* Footer Info */}
      <div className="p-6 border-t border-slate-800 text-xs text-slate-500">
        FOSSEE IIT Bombay<br/>2024 &copy; All rights reserved.
      </div>
    </div>
  );
};

export default Sidebar;