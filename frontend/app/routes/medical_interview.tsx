import { useState, useEffect } from "react";
import type { Route } from "../+types/root";

import { IntakeChat } from "./intakeChat";

export async function clientLoader({ request, params }: Route.ClientLoaderArgs) {
    const res = await fetch(`/api/medical_interviews/${params.interviewId}`);
    const interviewForm = await res.json();
    const initialMessage = interviewForm.initial_consult
    return { initialMessage }
}

export default function MedicalInterview({ loaderData, params }: Route.ComponentProps) {
    const interviewId = params.interviewId ?? ""
    const [interviewForm, setInterviewForm] = useState(null);
    const [flash, setFlash] = useState(false);

    const responseEndHandler = async () => {
        const res = await fetch(`/api/medical_interviews/${interviewId}`);
        const data = await res.json();
        setInterviewForm(data);
    }

    // useEffect(() => {
    //     responseEndHandler();
    // }, [])

    useEffect(() => {
        if (!interviewForm) {
            responseEndHandler();
            return
        };
        setFlash(true);
        const t = window.setTimeout(() => setFlash(false), 3000);
        return () => window.clearTimeout(t);
    }, [interviewForm]);

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
            <div className="w-2/5 border-r">
                <IntakeChat interviewId={interviewId} initialMessage={loaderData.initialMessage} responseEndHandler={responseEndHandler} />
            </div>

            {/* 右：問診表 */}
            <div className="w-3/5 p-4 overflow-auto">
                <div className="font-semibold mb-2">Medical Interview Form</div>
                {/* <div>{interviewForm || "（まだデータがありません）"}</div> */}
                <div
                    className={[
                        "transition-colors",
                        flash ? "bg-yellow-100 animate-pulse" : "bg-white",
                    ].join(" ")}
                >
                    <pre className="whitespace-pre-wrap text-sm">
                        {interviewForm ? JSON.stringify(interviewForm, null, 2) : "（まだデータがありません）"}
                    </pre>
                </div>
            </div>
        </div>
    )
}