import type { Route } from "../+types/root";
import { Link, useFetcher } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";

export async function clientLoader({ request, params }: Route.ClientLoaderArgs) {
    const res = await fetch(`/api/job-boards/${params.jobBoardId}/job-posts`);
    const jobPosts = await res.json();
    return { jobPosts }
}

export default function JobPosts({ loaderData, params }: Route.ComponentProps) {
    const fetcher = useFetcher();

    return (
        <div className="p-4 max-w-5xl mx-auto">
            <Button className="float-right">
                <Link to={`/job-boards/${params.jobBoardId}/add-job`}>Add Job</Link>
            </Button>
            <Table className="mt-4">
                <TableHeader>
                    <TableRow>
                        <TableHead className="max-w-sm">Title</TableHead>
                        <TableHead className="max-w-xs">Description</TableHead>
                        <TableHead>Status</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {loaderData.jobPosts.map(
                        (jobPost) =>
                            <TableRow key={jobPost.id}>
                                <TableCell className="">
                                    <Link to={`/job-boards/${jobPost.job_board_id}/job-posts/${jobPost.id}`}>
                                        {jobPost.title}
                                    </Link>
                                </TableCell>
                                <TableCell className="max-w-md truncate">
                                    {jobPost.description}
                                </TableCell>
                                <TableCell>
                                    {jobPost.status}
                                </TableCell>
                            </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    )
}
