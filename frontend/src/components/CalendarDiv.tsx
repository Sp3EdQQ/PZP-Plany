import { useState } from "react"
import { Calendar } from "@/components/ui/calendar"

export const CalendarDiv = () => {
  const [date, setDate] = useState<Date | undefined>(new Date())
  const currentDate = new Date()
  const currentDay = currentDate.getDay()
  const currentMonth = String(currentDate.getMonth() + 1).padStart(2, "0")
  const currentYear = String(currentDate.getFullYear())
  console.log(date)

  return (<div className="w-1/5 flex-col m-6">
    <Calendar
      mode="single"
      selected={date}
      onSelect={setDate}
      className="rounded-md border w-64"
    />
    <div className="pt-1">
      Dzisiaj mamy {currentDay}.{currentMonth}.{currentYear}
    </div>
  </div>)

}