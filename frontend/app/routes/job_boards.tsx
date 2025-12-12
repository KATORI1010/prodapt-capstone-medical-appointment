import type { Route } from "../+types/root";
import { Link, useFetcher, type ClientLoaderFunctionArgs } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { userContext } from "~/context";

export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
    const me = context.get(userContext);
    const isAdmin = me && me.is_admin;
    const res = await fetch(`/api/job-boards`);
    const jobBoards = await res.json();
    return { jobBoards, isAdmin }
}

export async function clientAction({ request }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const jobBoardId = formData.get("job_board_id");
    await fetch(`/api/job-boards/${jobBoardId}`, {
        method: "DELETE",
    })
}

export default function JobBoards({ loaderData }: Route.ComponentProps) {
    const fetcher = useFetcher();

    return (
        <div className="w-full items-center justify-center flex">
            <div className="p-4 max-w-3xl min-w-2xl">
                {loaderData.isAdmin
                    ? (<div className="float-right">
                        <Button>
                            <Link to="/job-boards/new">Add New Job Board</Link>
                        </Button>
                    </div>)
                    : <></>
                }
                {/* <Table className="w-1/2"> */}
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Logo</TableHead>
                            <TableHead>Slug</TableHead>
                            <TableHead></TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {loaderData.jobBoards.map(
                            (jobBoard) =>
                                <TableRow key={jobBoard.id}>
                                    <TableCell>
                                        {jobBoard.logo_url
                                            ? <Avatar><AvatarImage src={jobBoard.logo_url}></AvatarImage></Avatar>
                                            : <></>}
                                    </TableCell>
                                    <TableCell><Link to={`/job-boards/${jobBoard.id}/job-posts`} className="capitalize">{jobBoard.slug}</Link></TableCell>
                                    <TableCell>
                                        <div className="flex gap-8">
                                            <Link to={`/job-boards/${jobBoard.id}/edit`} className="capitalize">Edit</Link>
                                            <fetcher.Form method="post"
                                                onSubmit={(event) => {
                                                    const response = confirm(
                                                        `Please confirm you want to delete this job board '${jobBoard.slug}'.`,
                                                    );
                                                    if (!response) {
                                                        event.preventDefault();
                                                    }
                                                }}
                                            >
                                                <input name="job_board_id" type="hidden" value={jobBoard.id}></input>
                                                <button className="cursor-pointer">Delete</button>
                                            </fetcher.Form>
                                        </div>
                                    </TableCell>
                                </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
        </div>
    )
}