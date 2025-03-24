import { getCurrentWindow } from "@tauri-apps/api/window";
import { useEffect, useState } from "react";

function TitleBar() {
  const appWindow = getCurrentWindow();
  const titlebarIcons = {
    logo: (
      <svg
        data-tauri-drag-region
        className="h-6 w-12"
        viewBox="-2 -2 24.00 24.00"
        xmlns="http://www.w3.org/2000/svg"
        fill="#fee685"
      >
        <path
          data-tauri-drag-region
          transform="translate(-44.000000, -4400.000000)"
          d="M46.938,4411.948 L53,4403.804 L53,4415.5 L46.938,4411.948 Z M61.063,4411.948 L55,4415.5 L55,4403.804 L61.063,4411.948 Z M55.001,4400.454 L54,4399 L53,4400.454 L44,4412.545 L53,4417.818 L54,4418.357 L55.001,4417.818 L64,4412.545 L55.001,4400.454 Z"
        ></path>
      </svg>
    ),
    maximize: (
      <svg
        className="h-6 w-6"
        fill="currentColor"
        viewBox="0 0 36 36"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M27.89,9h-20a2,2,0,0,0-2,2V25a2,2,0,0,0,2,2h20a2,2,0,0,0,2-2V11A2,2,0,0,0,27.89,9Zm-20,16V11h20V25Z"></path>{" "}
      </svg>
    ),
    restore: (
      <svg
        className="h-6 w-6"
        fill="currentColor"
        viewBox="0 0 36 36"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M28,8H14a2,2,0,0,0-2,2v2h2V10H28V20H26v2h2a2,2,0,0,0,2-2V10A2,2,0,0,0,28,8Z"></path>
        <path d="M22,14H8a2,2,0,0,0-2,2V26a2,2,0,0,0,2,2H22a2,2,0,0,0,2-2V16A2,2,0,0,0,22,14ZM8,26V16H22V26Z"></path>
      </svg>
    ),
    minimize: (
      <svg
        className="h-6 w-6"
        fill="currentColor"
        viewBox="0 0 36 36"
        xmlns="http://www.w3.org/2000/svg"
        data-darkreader-inline-fill=""
      >
        <path d="M27,27H9a1,1,0,0,1,0-2H27a1,1,0,0,1,0,2Z"></path>{" "}
      </svg>
    ),
    close: (
      <svg
        className="h-6 w-6"
        fill="currentColor"
        viewBox="0 0 36 36"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M19.41,18l7.29-7.29a1,1,0,0,0-1.41-1.41L18,16.59,10.71,9.29a1,1,0,0,0-1.41,1.41L16.59,18,9.29,25.29a1,1,0,1,0,1.41,1.41L18,19.41l7.29,7.29a1,1,0,0,0,1.41-1.41Z"></path>{" "}
      </svg>
    ),
  };
  const [isMaximized, setIsMaximized] = useState(false);

  useEffect(() => {
    async function checkMaximized() {
      setIsMaximized(await appWindow.isMaximized());
    }

    checkMaximized();

    window.addEventListener("resize", checkMaximized);
  }, []);

  function LeftTitlebarButtons() {
    return (
      <>
        <button
          onClick={() => appWindow.minimize()}
          className="mr-2 ml-2 inline-flex h-7.5 w-7.5 items-center justify-center text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
        >
          {titlebarIcons.minimize}
        </button>
        <button
          onClick={() => appWindow.toggleMaximize()}
          className="mr-2 ml-2 inline-flex h-7.5 w-7.5 items-center justify-center text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
        >
          {isMaximized ? titlebarIcons.restore : titlebarIcons.maximize}
        </button>
        <button
          onClick={() => appWindow.close()}
          className="mr-2 ml-2 inline-flex h-7.5 w-7.5 items-center justify-center text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
        >
          {titlebarIcons.close}
        </button>
      </>
    );
  }

  return (
    <div
      data-tauri-drag-region
      className="fixed top-0 right-0 left-0 flex h-7.5 justify-between border-b border-neutral-700 bg-neutral-900"
    >
      <div
        data-tauri-drag-region
        id="left-space"
        className="inline-flex h-7.5 items-center justify-center"
      >
        {titlebarIcons.logo}
      </div>
      <div
        data-tauri-drag-region
        id="center-space"
        className="h-7.5 flex-grow items-center text-center font-medium text-gray-500 select-none dark:text-gray-400"
      >
        &lt; Cassandra &gt;
      </div>
      <div id="right-space">
        <LeftTitlebarButtons />
      </div>
    </div>
  );
}

export default TitleBar;
