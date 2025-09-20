const StartPanel = () => {
  return (
    <div className="h-4/5 w-full flex flex-col items-center justify-start text-center space-y-6">
      <div
        className="h-3/5 w-full bg-grey font-mono p-10 flex flex-col items-center justify-center relative"
        data-augmented-ui="tr-clip tl-2-clip-x br-2-clip-y bl-2-clip-x both"
      >
        <h1 className="text-3xl font-bold tracking-widest">POKE TYPER CNN</h1>
        <p className="mt-2 text-lg opacity-80">by Bryan Yee</p>

        <svg
          className="absolute bottom-4 left-1/2 -translate-x-1/2"
          width="120"
          height="2"
          viewBox="0 0 120 2"
          xmlns="http://www.w3.org/2000/svg"
        >
          <line
            x1="0"
            y1="1"
            x2="120"
            y2="1"
            stroke="white"
            strokeWidth="2"
            strokeDasharray="6 4"
          />
        </svg>
      </div>
    </div>
  );
};

export default StartPanel;
