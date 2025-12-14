import { useState, useEffect } from "react";
import type { Route } from "../+types/root";

import { IntakeChat } from "./intakeChat";

export default function MedicalInterview({ params }: Route.ComponentProps) {
    const interviewId = params.interviewId ?? ""
    const [interviewForm, setInterviewForm] = useState(null);

    const responseEndHandler = async () => {
        const res = await fetch(`/api/medical_interviews/${interviewId}`);
        const data = await res.json();
        setInterviewForm(data);
    }

    useEffect(() => {
        responseEndHandler();
    }, [])

    // alert(interviewId);
    return (
        // <div className="w-full flex flex-col">
        //     <div className="max-w-3xl mx-auto my-8">
        //         <IntakeChat interviewId={interviewId} />
        //     </div>
        //     <div>
        //         qqq
        //         {interviewForm}
        //     </div>
        // </div>
        <div className="h-screen w-full flex">
            {/* 左：Chat */}
            <div className="w-1/2 p-4 border-r">
                <IntakeChat interviewId={interviewId} responseEndHandler={responseEndHandler} />
            </div>

            {/* 右：問診表 */}
            <div className="w-1/2 p-4 overflow-auto">
                <div className="font-semibold mb-2">問診表</div>
                {/* <div>{interviewForm || "（まだデータがありません）"}</div> */}
                <pre className="whitespace-pre-wrap">
                    {interviewForm ? JSON.stringify(interviewForm, null, 2) : "（まだデータがありません）"}
                </pre>
            </div>
        </div>
    )
}