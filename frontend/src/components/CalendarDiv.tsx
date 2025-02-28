import { useState } from "react"
import { Calendar } from "@/components/ui/calendar"

export const CalendarDiv = () => {
  const [date, setDate] = useState<Date | undefined>(new Date())
  const marginForCalendar: number = 5
  return (<div className={`w-1/5 ml-${marginForCalendar} mt-${marginForCalendar}`}>
    <Calendar
      mode="single"
      selected={date}
      onSelect={setDate}
      className="rounded-md border w-64"
    />
  </div>)

}