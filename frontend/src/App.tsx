import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Main from "./components/Main";
import Datos from "./components/Datos";
import Ppto from "./components/Ppto";
import Apu from "./components/Apu";
import Insumos from "./components/Insumos";
import Gastos from "./components/Gastos";
import Config from "./components/Config";
import TitleBar from "./components/Titlebar";
import { getCurrentWindow, LogicalSize } from "@tauri-apps/api/window";

await getCurrentWindow().setMinSize(new LogicalSize(800, 600));

function App() {
  const [sidebarStatus, setSidebarStatus] = useState(false);
  const [activeComponent, setActiveComponent] = useState("Main");
  const componentMap: { [key: string]: React.JSX.Element } = {
    Datos: <Datos />,
    Ppto: <Ppto />,
    Apu: <Apu />,
    Insumos: <Insumos />,
    Gastos: <Gastos />,
    Config: <Config />,
  };

  return (
    <div className="flex h-dvh bg-neutral-50 font-light text-gray-200 dark:bg-neutral-800">
      <TitleBar />
      <div
        className={`fixed top-7.5 bottom-0 left-0 ${sidebarStatus ? "w-52" : "w-12.5"}`}
      >
        <Sidebar
          component={activeComponent}
          activateComponent={setActiveComponent}
          sidebarStatus={sidebarStatus}
          setSidebarStatus={setSidebarStatus}
        />
      </div>
      <div
        className={`fixed top-7.5 right-0 bottom-0 bg-red-300 ${sidebarStatus ? "left-52" : "left-12.5"}`}
      >
        {componentMap[activeComponent] || <Main />}
      </div>
    </div>
  );
}

export default App;
