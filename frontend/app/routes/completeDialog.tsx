import { Link } from "react-router"
import { Button } from "~/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "~/components/ui/dialog"
import { Input } from "~/components/ui/input"
import { Label } from "~/components/ui/label"
import { ScrollArea } from "~/components/ui/scroll-area"

type CompleteDialogType = {
    open: boolean;
    setOpen: (value: boolean) => void;
    interviewForm: string;
}


export function CompleteDialog({ open, setOpen, interviewForm }: CompleteDialogType) {
    return (
        <Dialog open={open} onOpenChange={setOpen} >
            <DialogContent className="sm:max-w-3xl h-3/4">
                <DialogHeader>
                    <DialogTitle>Medical interview completed</DialogTitle>
                    <DialogDescription>
                        The medical intake will be registered with the following information.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4">
                    <ScrollArea className="h-80 w-full rounded-md border">
                        <pre className="whitespace-pre-wrap text-sm">
                            {interviewForm ? JSON.stringify(interviewForm, null, 2) : "（まだデータがありません）"}
                        </pre>
                    </ScrollArea>
                </div>
                <DialogFooter>
                    <DialogClose asChild>
                        <Button variant="outline" className="cursor-pointer">Cancel</Button>
                    </DialogClose>
                    <Button type="button"><Link to="/">Complete</Link></Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
