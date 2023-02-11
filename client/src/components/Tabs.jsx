import React, { useState } from "react";

const Tabs = ({ tabs, children }) => {
  const [selectedTab, setSelectedTab] = useState(0);

  return (
    <div className="">
      <div className="bg-gray-300 py-2">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setSelectedTab(index)}
            className={`px-4 py-2 hover:bg-gray-400 ${
              selectedTab === index ? "bg-gray-400" : ""
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="bg-white w-full">{children[selectedTab]}</div>
    </div>
  );
};

export default Tabs;
