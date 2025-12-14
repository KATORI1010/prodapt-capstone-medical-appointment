import type { Route } from "../+types/root";

import { IntakeChat } from "./intakeChat";

export default function MedicalInterview({ params }: Route.ComponentProps) {
    const interviewId = params.interviewId ?? ""
    // alert(interviewId);
    return (
        <div className="w-full text-center">
            {/* <h1 className="mt-16 scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance">
                May I help you?
            </h1> */}
            <div className="max-w-3xl mx-auto my-8">
                <IntakeChat interviewId={interviewId}/>
            </div>
            {/* <IntakeChat /> */}
        </div>
        // <IntakeChat />
    )
}