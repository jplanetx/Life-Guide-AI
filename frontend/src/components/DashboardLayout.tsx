import React, { useState, ReactNode } from 'react';
import { Menu, X, ChevronRight, ChevronLeft } from 'lucide-react';

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [detailsOpen, setDetailsOpen] = useState(false);

  return (
    <div className="h-screen flex overflow-hidden bg-gray-100">
      {/* Left Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-16'} transition-all duration-200 bg-white border-r`}>
        <div className="h-16 flex items-center justify-between px-4 border-b">
          <h2 className={`font-medium ${sidebarOpen ? 'block' : 'hidden'}`}>Life Guide AI</h2>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-1 rounded hover:bg-gray-100"
          >
            {sidebarOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="p-4">
          <ul className="space-y-2">
            <li className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded cursor-pointer">
              <Menu size={20} />
              {sidebarOpen && <span>All Tasks</span>}
            </li>
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        <main className="flex-1 overflow-y-auto p-4">
          {children}
        </main>

        {/* Right Details Panel */}
        {detailsOpen && (
          <div className="w-80 border-l bg-white p-4 overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-medium">Task Details</h3>
              <button
                onClick={() => setDetailsOpen(false)}
                className="p-1 rounded hover:bg-gray-100"
              >
                <X size={20} />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardLayout;
