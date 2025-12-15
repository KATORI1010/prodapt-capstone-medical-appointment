import { useState, useEffect } from "react";
import type { Route } from "../+types/root";

import { IntakeChat } from "./intakeChat";
import { CompleteDialog } from "./completeDialog";

export async function clientLoader({ request, params }: Route.ClientLoaderArgs) {
    const res = await fetch(`/api/medical_interviews/${params.interviewId}`);
    const interviewForm = await res.json();
    const initialMessage = interviewForm.initial_consult
    return { initialMessage }
}

export default function MedicalInterview({ loaderData, params }: Route.ComponentProps) {
    const interviewId = params.interviewId ?? ""
    const [interviewForm, setInterviewForm] = useState("");
    const [flash, setFlash] = useState(false);
    const [completed, setCompleted] = useState(false);

    const responseEndHandler = async () => {
        const res = await fetch(`/api/medical_interviews/${interviewId}`);
        const data = await res.json();
        setInterviewForm(data.intake);
    }

    const effectHander = ({ name, data }: { name: string, data: string }) => {
        if (name === "interview_completed") {
            setCompleted(true);
        }
    }

    useEffect(() => {
        if (!interviewForm) {
            responseEndHandler();
            return
        };
        setFlash(true);
        const t = window.setTimeout(() => setFlash(false), 3000);
        return () => window.clearTimeout(t);
    }, [interviewForm]);

    return (
        <div className="h-screen w-full flex">
            {/* 左：Chat */}
            <div className="w-1/2 border-r">
                <IntakeChat
                    interviewId={interviewId}
                    initialMessage={loaderData.initialMessage}
                    responseEndHandler={responseEndHandler}
                    effectHander={effectHander}
                />
            </div>

            {/* 右：問診表 */}
            <div className="w-1/2 p-4 overflow-auto">
                <div className="font-semibold mb-2">Medical Interview Form</div>
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
            <CompleteDialog open={completed} setOpen={setCompleted} interviewForm={interviewForm} />
        </div>
    )
}