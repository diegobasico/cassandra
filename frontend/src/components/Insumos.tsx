import { register, isRegistered, unregister } from "@tauri-apps/plugin-global-shortcut";
import { useEffect } from "react";

async function setupShortcut() {
  const shortcut = "CommandOrControl+M";

  const alreadyRegistered = await isRegistered(shortcut);
  if (alreadyRegistered) {
    await unregister(shortcut);
  }

  let isHandlingShortcut = false;

  await register(shortcut, () => {
    if (!isHandlingShortcut) {
      isHandlingShortcut = true;
      console.log("Shortcut triggered");

      setTimeout(() => {
        isHandlingShortcut = false;
      }, 100);
    }
  });

  console.log(`Shortcut ${shortcut} registered successfully.`);
}

function Insumos() {
  useEffect(() => {
    setupShortcut();
    return () => {
      unregister("CommandOrControl+M").catch(console.error);
    };
  }, []);
  return (
    <div className="p-4">
      <span className="text-3xl text-wrap">Insumos</span>
    </div>
  );
}

export default Insumos;
