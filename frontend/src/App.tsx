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
import { getCurrentWindow, PhysicalSize } from "@tauri-apps/api/window";

await getCurrentWindow().setMinSize(new PhysicalSize(960, 720));

function App() {
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
    <div className="flex h-dvh flex-col bg-neutral-50 font-light text-gray-200 dark:bg-neutral-800">
      <TitleBar />
      <div className="mt-7.5 flex flex-grow overflow-hidden">
        <Sidebar component={activeComponent} activateComponent={setActiveComponent} />
        {componentMap[activeComponent] || <Main />}
      </div>
    </div>
  );
}

export default App;
