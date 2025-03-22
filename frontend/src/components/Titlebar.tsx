import { ReactNode } from "react";
import { getCurrentWindow } from "@tauri-apps/api/window";

function TitleBar() {
  interface titleBarButtonProps {
    svg: ReactNode;
    action: () => void;
  }

  const appWindow = getCurrentWindow();

  const rightTitlebarButtons: titleBarButtonProps[] = [
    {
      svg: (
        <svg
          className="h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M20 14H4v-4h16" />
        </svg>
      ),
      action: () => appWindow.minimize(),
    },
    {
      svg: (
        <svg
          className="h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M4 4h16v16H4zm2 4v10h12V8z" />
        </svg>
      ),
      action: () => appWindow.toggleMaximize(),
    },
    {
      svg: (
        <svg
          className="h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12z" />
        </svg>
      ),
      action: () => appWindow.close(),
    },
  ];

  const logo: { svg: ReactNode } = {
    svg: (
      <svg
        data-tauri-drag-region
        className="ml-2 h-5 w-5"
        fill="currentColor"
        viewBox="0 0 20 20"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          data-tauri-drag-region
          transform="translate(-44.000000, -4400.000000)"
          d="M46.938,4411.948 L53,4403.804 L53,4415.5 L46.938,4411.948 Z M61.063,4411.948 L55,4415.5 L55,4403.804 L61.063,4411.948 Z M55.001,4400.454 L54,4399 L53,4400.454 L44,4412.545 L53,4417.818 L54,4418.357 L55.001,4417.818 L64,4412.545 L55.001,4400.454 Z"
        ></path>
      </svg>
    ),
  };

  function TitlebarButton({ icons }: { icons: titleBarButtonProps[] }) {
    return (
      <>
        {icons.map((item, index) => (
          <div
            className="mr-2 ml-2 inline-flex h-7.5 w-7.5 items-center justify-center"
            key={index}
          >
            <button
              id={`titlebar-button-${index}`}
              onClick={item.action}
              className="text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
            >
              {item.svg}
            </button>
          </div>
        ))}
      </>
    );
  }

  return (
    <div
      data-tauri-drag-region
      className="flex h-7.5 justify-between border-b border-neutral-700 bg-neutral-900"
    >
      <div
        data-tauri-drag-region
        id="left-space"
        className="inline-flex h-7.5 w-7.5 items-center justify-center text-amber-200"
      >
        {logo.svg}
      </div>
      <div
        data-tauri-drag-region
        id="center-space"
        className="h-7.5 flex-grow items-center text-center font-medium text-gray-500 select-none dark:text-gray-400"
      >
        &lt; Cassandra &gt;
      </div>
      <div id="right-space">
        <TitlebarButton icons={rightTitlebarButtons} />
      </div>
    </div>
  );
}

export default TitleBar;
