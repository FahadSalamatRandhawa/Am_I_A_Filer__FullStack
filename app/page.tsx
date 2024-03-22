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
import { Toaster } from "@/components/ui/toaster"

import { useState } from "react";
import { useToast } from "@/components/ui/use-toast";
import { title } from "process";

export default function Home() {
  const [value,setValue]=useState<string|null>(null)
  const [filter,setFilter]=useState<string|null>(null)
  const [answer,setAnswer]=useState<Array<unknown>|null>(null)

  const {toast}=useToast()

  async function Check_Filer(){
    setAnswer(null)

    //Api call
    const requestbody=JSON.stringify({"filter":filter,"value":value})
    console.log(requestbody)
    const apiCall=await fetch("/api/check",{method:"POST",headers: {
      'Content-Type': 'application/json' // Specify that the body is JSON.
    },
    body:requestbody})


    // if error notify and console log error
    if(!apiCall.ok){
      let apiResponse=await apiCall.json()
      console.log(apiResponse.error)
      toast({
        title:'Error',
        description:apiResponse.details,
      })
    }else{
      const apiResponse=await apiCall.json()
      if(apiResponse.success){
        setAnswer(apiResponse.data)
      }else{ //if not sucessful
        toast({
          title: 'Not successful',
          description: apiResponse.message,
        })
      }
      console.log(apiResponse)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-10 gap-5 lg:gap-10">
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

      <div className=" flex flex-col gap-4 lg:gap-6 ">
        {
          answer&&answer.map((item:any,index)=>(
            
            <div className=" flex flex-wrap gap-2 border-b-yellow-600 border-b">
            {index+1} | {
                Object.keys(item).map((key)=>(
                  <text className="w-auto">{key} : {item[key]}</text>
                ))
              }
            </div>
          ))
        }
      </div>
      <Toaster/>
    </main>
  );
}
