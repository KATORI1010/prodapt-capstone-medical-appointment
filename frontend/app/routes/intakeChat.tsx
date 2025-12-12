// IntakeChat.tsx
import { ChatKit, useChatKit } from "@openai/chatkit-react";

const options = {
    theme: {
        typography: {
            fontFamily: "'Inter', sans-serif",  // フォント指定
            // ※ 文字サイズ自体は fontSize など別プロパティが用意されている場合もあります
        },
        density: "comfortable",   // 余白のサイズ
        colorScheme: "light",
    },
};

export function IntakeChat() {
    const { control } = useChatKit({
        api: {
            url: "/chatkit",
            domainKey: "local-dev",
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
    });

    return <ChatKit control={control} className="h-[80vh] w-full text-sm" />;
}
