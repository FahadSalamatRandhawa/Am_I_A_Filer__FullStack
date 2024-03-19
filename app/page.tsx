"use client"
import { Button } from "@/components/ui/button";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { useState } from "react";

export default function Home() {
  const [value,setValue]=useState<string|null>(null)
  const [filter,setFilter]=useState<string|null>(null)

  async function Check_Filer(){
    const requestbody=JSON.stringify({"filter":filter,"value":value})
    console.log(requestbody)
    const apiCall=await fetch("/api/check",{method:"POST",headers: {
      'Content-Type': 'application/json' // Specify that the body is JSON.
    },
    body:requestbody})
    if(!apiCall.ok){
      console.log("Error in api call");
    }else{
      const apiResponse=await apiCall.json()
      console.log(apiResponse)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex gap-3 items-center">
        <Input onChange={(e)=>setValue(e.target.value)} />

        <Select onValueChange={(e)=>setFilter(e)}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Search by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="NTN">NTN</SelectItem>
            <SelectItem value="NAME">NAME</SelectItem>
            <SelectItem value="CNIC">CNIC</SelectItem>
            <SelectItem value="BUSINESS NAME">BUSINESS NAME</SelectItem>
          </SelectContent>
        </Select>

        <Button disabled={!value || !filter} onClick={Check_Filer} >Check</Button>
      </div>
    </main>
  );
}
