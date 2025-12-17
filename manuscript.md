# Manuscript for explaining the system

## Overview
> First, I will briefly explain the problem this system is trying to solve.

> Before a clinic visit, patient information is often collected manually and is not always complete.<br>
> Because of this, doctors have to repeat many basic questions during the appointment.<br>

> I was also hospitalized this past July, and I was asked the same questions many times during medical interviews.<br>
> It was frustrating a little.

> To address this problem, I built a multi-turn conversational AI system for medical intake.<br>
> At a high level, the system consists of two AI agents: a Medical Interview Agent and a Reviewer Agent.<br>
> The Medical Interview Agent talks with the patient and fills an intake form, which is stored in a database.<br>
> The Reviewer Agent then checks whether the intake information is sufficient.

> Now, let me show you a short demo.

---
## Demo
> This is the demo top page. Since this is a prototype, the login and appointment creation features are mockups.
<br>-> これはデモ用のトップページです。プロトタイプなのでログイン機能と予約作成の機能はモックです。

> First, patients are asked to enter their medical condition and concerns in a free-form format.
<br>-> 初めに患者さんにフリーフォーマットで自身の病状や困っていることを入力してもらいます。

> Pressing the Next button will launch the chat screen and post the content patients just entered.
<br>-> Nextボタンを押すとチャット画面が起動し、先ほど入力した内容がチャットに投稿されます。

> As you can see, the left side shows the chat UI, while the right side displays the Intake Form data stored in the database.
<br>-> ご覧いただけるように、左側はチャットのUIで、右側はDBに保存されている問診票のデータが表示されるようになっています。

> The agent is asking me this question, so I'll respond.
<br>-> エージェントが私に質問してきているので回答します。

> When the patient responds to the agent’s questions, the agent updates the intake form data in the database in real time.
<br>-> Agentからの質問に回答すると、AgentはDBのデータを更新します。

> The agent keeps asking follow-up questions to gather more details about symptoms, medications, and allergies.
<br>-> Agentは内容の深堀を続けて、症状の詳細や薬、アレルギーのヒアリングを行います。

> Since time is limited, we will switch to an intake form that has already been fully filled through prior interviews, and demonstrate how the Reviewer Agent works and how the interview is closed.
<br>-> 時間が限られるので、事前に十分に問診を行っているデータに変更して、レビューAgentと問診のクローズについてデモをします。

> When the system determines that the intake form contains sufficient information, it sends the form to the Reviewer Agent for review.<br>
> If the review passes, the chat is closed and the medical interview is completed.
<br>-> Intake Formデータが十分と判断した場合は、Reviewer Agentにレビューを依頼します。 合格であれば、チャットをクローズして問診を完了させます。

---
## Architecture Explanation

> Next, I'd like to explain the architecture and mechanism.
<br>-> 次にアーキテクチャと仕組みについて説明します。

> First,I will explain the characteristics of the Agent implementation.
<br>-> 初めに、Agentの実装の特徴について説明します。

> At first, the Medical Interview Agent did not ask deep enough questions about patient symptoms.<br>
> To improve this, I updated the prompt so that the agent asks questions following the OPQRST framework.<br>
> OPQRST is a simple structure that helps describe a symptom by covering when it started, how it feels, how strong it is, where it is, and how it changes over time.

> This is the architecture of the system.<br>
> The main components are a frontend built with React Router, a backend built with FastAPI, and a PostgreSQL database.<br>
> One key characteristic of this system is that OpenAI Chatkit is integrated on both the frontend and the backend sides.

> Chatkit is an OpenAI-provided feature that lets us easily embed a chat interface connected to AI agents, out of the box.<br>
> It provides ready-to-use React components, so we can simply incorporate them into our frontend.

---
## Why use Chatkit?
> Finally, I’d like to explain why I chose Chatkit.

> Implementing a chat UI with streaming can take a lot of time, so I used Chatkit to build it quickly.

> Chatkit also integrates well with the OpenAI Agents SDK, which makes it easy to connect the agents to the chat screen.

