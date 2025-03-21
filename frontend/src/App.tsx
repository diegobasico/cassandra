import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Main from "./components/Main";
import Datos from "./components/Datos";
import Ppto from "./components/Ppto";
import Apu from "./components/Apu";
import Insumos from "./components/Insumos";
import Gastos from "./components/Gastos";
import Config from "./components/Config";

function App() {
  const [activeComponent, setActiveComponent] = useState<string>("Main");

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
      <Sidebar activateComponent={setActiveComponent} />
      {componentMap[activeComponent] || <Main />}
    </div>
  );
}

export default App;
