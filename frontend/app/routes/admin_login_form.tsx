import { cn } from "~/lib/utils"
import { Button } from "~/components/ui/button"
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "~/components/ui/card"
import {
    Field,
    FieldGroup,
    FieldLabel,
} from "~/components/ui/field"
import { Input } from "~/components/ui/input"
import { Form, redirect } from "react-router"
import type { Route } from "../+types/root"

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData()
    await fetch(`/api/admin-login`, {
        method: 'POST',
        body: formData,
    })
    return redirect("/job-boards")
}

export default function LoginForm({
    className,
    ...props
}: React.ComponentProps<"div">) {
    return (
        <div className={cn("flex flex-col gap-6 w-1/3 mx-auto mt-4", className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Admin Login</CardTitle>
                </CardHeader>
                <CardContent>
                    <Form method="post">
                        <FieldGroup>
                            <Field>
                                <FieldLabel htmlFor="username">Username</FieldLabel>
                                <Input
                                    id="username"
                                    name="username"
                                    type="text"
                                    required
                                />
                            </Field>
                            <Field>
                                <div className="flex items-center">
                                    <FieldLabel htmlFor="password">Password</FieldLabel>
                                </div>
                                <Input id="password" name="password" type="password" required />
                            </Field>
                            <Field>
                                <Button type="submit">Login</Button>
                            </Field>
                        </FieldGroup>
                    </Form>
                </CardContent>
            </Card>
        </div>
    )
}
