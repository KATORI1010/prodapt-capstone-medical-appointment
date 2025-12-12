import { useState, useEffect } from "react";

import type { Route } from "../+types/root";
import { Link, useActionData, useFetcher } from "react-router";
import { Avatar, AvatarImage } from "~/components/ui/avatar";
import { Button } from "~/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";

export async function clientLoader({ request, params }: Route.ClientLoaderArgs) {
    const res1 = await fetch(`/api/job-posts/${params.jobPostId}`);
    const jobPost = await res1.json();
    const res2 = await fetch(`/api/job-posts/${params.jobPostId}/job-applications`);
    const jobApplications = await res2.json();
    return { jobPost, jobApplications }
}

export async function clientAction({ request, params }: Route.ClientActionArgs) {
    const formData = await request.formData();
    const job_post_id = formData.get("job_post_id");
    const response = await fetch(`/api/job-posts/${job_post_id}/recommend`)
    const result = await response.json()
    return { "recommend": result }
}

type RecommendType = {
    id: number;
    email: string;
    job_post_id: number;
    last_name: string;
    first_name: string;
    resume_url: string;
}

export default function JobPostsDetail({ loaderData, params }: Route.ComponentProps) {
    const fetcher = useFetcher();

    const [recommend, setRecommend] = useState<RecommendType[]>([])

    const actionData = useActionData();

    useEffect(() => {
        if (fetcher.data?.recommend) {
            setRecommend([{ ...fetcher.data?.recommend }]);
        }
    }, [fetcher.data]);

    return (
        <div className="p-4 max-w-5xl mx-auto">
            <div className="flex justify-between items-center pb-2 border-b">
                <h2 className="scroll-m-20 text-3xl font-semibold tracking-tight first:mt-0">
                    {loaderData.jobPost.title}
                </h2>
                <div className="flex gap-2">
                    <Button>
                        <Link to={`add-application`}>Apply</Link>
                    </Button>
                    <fetcher.Form method="post"
                        onSubmit={(event) => {
                            const response = confirm(
                                `Do you launch recommendation AI for Job "${loaderData.jobPost.title}"?`,
                            );
                            if (!response) {
                                event.preventDefault();
                            }
                        }}
                    >
                        <input name="job_post_id" type="hidden" value={loaderData.jobPost.id}></input>
                        <Button className="cursor-pointer">Get Recommendation</Button>
                    </fetcher.Form>
                    <Button variant="outline">
                        <Link to=".." relative="path">Back</Link>
                    </Button>
                </div>
            </div>
            <p className="leading-7 [&:not(:first-child)]:mt-6">
                {loaderData.jobPost.description}
            </p>
            {recommend?.length > 0 &&
                <div>
                    <h3 className="scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight mt-8">
                        Recommended Application
                    </h3>
                    <Table className="mt-4 bg-yellow-100">
                        <TableHeader>
                            <TableRow>
                                <TableHead className="max-w-sm">ID</TableHead>
                                <TableHead className="max-w-xs">First Name</TableHead>
                                <TableHead className="max-w-xs">Last Name</TableHead>
                                <TableHead className="max-w-xs">Email</TableHead>
                                <TableHead className="max-w-xs">Resume</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {recommend.map(
                                (jobApplication) =>
                                    <TableRow key={jobApplication.id}>
                                        <TableCell className="max-w-md truncate">
                                            {jobApplication.id}
                                        </TableCell>
                                        <TableCell>
                                            {jobApplication.first_name}
                                        </TableCell>
                                        <TableCell>
                                            {jobApplication.last_name}
                                        </TableCell>
                                        <TableCell>
                                            {jobApplication.email}
                                        </TableCell>
                                        <TableCell>
                                            <Link to={jobApplication.resume_url} target="blank">
                                                {jobApplication.resume_url}
                                            </Link>
                                        </TableCell>
                                    </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </div>
            }
            <h3 className="scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight mt-8">
                Applications
            </h3>
            <Table className="my-4">
                <TableHeader>
                    <TableRow>
                        <TableHead className="max-w-sm">ID</TableHead>
                        <TableHead className="max-w-xs">First Name</TableHead>
                        <TableHead className="max-w-xs">Last Name</TableHead>
                        <TableHead className="max-w-xs">Email</TableHead>
                        <TableHead className="max-w-xs">Resume</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {loaderData.jobApplications.map(
                        (jobApplication) =>
                            <TableRow key={jobApplication.id}>
                                <TableCell className="max-w-md truncate">
                                    {jobApplication.id}
                                </TableCell>
                                <TableCell>
                                    {jobApplication.first_name}
                                </TableCell>
                                <TableCell>
                                    {jobApplication.last_name}
                                </TableCell>
                                <TableCell>
                                    {jobApplication.email}
                                </TableCell>
                                <TableCell>
                                    <Link to={jobApplication.resume_url} target="blank">
                                        {jobApplication.resume_url}
                                    </Link>
                                </TableCell>
                            </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    )
}
