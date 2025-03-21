function Main() {
  const hours: number = new Date().getHours();
  let timeOfDay: string;
  if (hours >= 5 && hours < 12) {
    timeOfDay = "morning";
  } else if (hours >= 12 && hours < 19) {
    timeOfDay = "afternoon";
  } else {
    timeOfDay = "night";
  }

  return <span className="p-4 text-3xl">Good {timeOfDay}</span>;
}

export default Main;
