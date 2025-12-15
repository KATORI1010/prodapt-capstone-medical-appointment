// IntakeChat.tsx
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import type { UseChatKitOptions } from "@openai/chatkit-react";

type IntakeChatProps = {
    interviewId: string;
    initialMessage?: string;
    responseEndHandler: (event: void) => void;
    effectHandler?: (event: {
        name: string;
        data?: Record<string, unknown>;
    }) => void;
}


export function IntakeChat({ interviewId, initialMessage, responseEndHandler, effectHandler }: IntakeChatProps) {
    const options: UseChatKitOptions = {
        api: {
            url: "/chatkit",
            domainKey: "local-dev",
            fetch: (input, init) =>
                fetch(input, {
                    ...init,
                    headers: {
                        ...(init?.headers || {}),
                        "x-interview-id": interviewId ?? "anonymous", // プロトタイプ用：そのまま渡す
                    },
                }),
            // async getClientSecret(existing) {
            //     // まずは最小：existingがあっても再発行でOK（後でrefresh最適化）
            //     // 公式例でも「existingがあればrefreshを実装」と記載があります :contentReference[oaicite:9]{index=9}
            //     const res = await fetch("/api/chatkit/session", {
            //         method: "POST",
            //         headers: { "Content-Type": "application/json" },
            //         body: JSON.stringify({ user: "local-dev-user" }),
            //     });
            //     const { client_secret } = await res.json();
            //     return client_secret;
            // },
        },
        onReady: () => {
            // 1通目のユーザーメッセージを自動化
            if (initialMessage) {
                sendUserMessage({
                    text: initialMessage,
                    newThread: true,
                });
            }
        },
        // チャットのレスポンス終了時に画面のデータ更新を行う
        onResponseEnd: responseEndHandler,
        onEffect: effectHandler,
        theme: {
            colorScheme: 'light',
            radius: 'pill',
            density: 'normal',
            color: {
                grayscale: {
                    hue: 52,
                    tint: 5,
                    shade: 2
                },
                // accent: {
                //     primary: '#1754cf',
                //     level: 1
                // }
            },
            typography: {
                baseSize: 14,
                fontFamily: '"OpenAI Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif',
                fontFamilyMono: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "DejaVu Sans Mono", "Courier New", monospace',
                fontSources: [
                    {
                        family: 'OpenAI Sans',
                        src: 'https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Regular.woff2',
                        weight: 400,
                        style: 'normal',
                        display: 'swap'
                    }
                    // ...and 7 more font sources
                ]
            }
        },
        history: {  // ヒストリー機能を無効化
            enabled: false,
            showDelete: false,
            showRename: false,
        },
        composer: {
            placeholder: 'Please respond to the medical question.',
            attachments: {  // ファイルの添付機能を無効化
                enabled: false
            },
            models: [
                {
                    id: "gpt-5-mini",
                    label: "gpt-5-mini",
                    description: "Light model",
                },
                {
                    id: "gpt-5.2",
                    label: "gpt-5.2",
                    description: "High performance",
                    default: true,
                },
            ],
        },
        startScreen: {
            greeting: 'What symptoms are troubling you?',
            prompts: [
                {
                    icon: 'notebook-pencil',
                    label: 'I have a fever.',
                    prompt: 'I have a fever.'
                },
                {
                    icon: 'notebook-pencil',
                    label: 'My stomach feels bad.',
                    prompt: 'My stomach feels bad.'
                }
                // ...and 4 more prompts
            ],
        },
        threadItemActions: {  // フィードバック機能を無効化
            feedback: false,
        },
    };

    const {
        control,
        setComposerValue,
        sendUserMessage,
        setThreadId,
    } = useChatKit(options);
    return <ChatKit control={control} className="h-full w-full" />;
}
