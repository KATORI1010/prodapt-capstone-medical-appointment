import { IntakeChat } from "./intakeChat";

export default function MedicalInterview() {
    return (
        <div className="w-full text-center">
            {/* <h1 className="mt-16 scroll-m-20 text-center text-4xl font-extrabold tracking-tight text-balance">
                May I help you?
            </h1> */}
            <div className="rounded-2xl border max-w-3xl mx-auto p-8 my-8"><IntakeChat /></div>
        </div>
    )
}