export interface PromptResponse {
    prompt: string;
}

export interface FileUploadResponse {
    message: string;
}

export class Server {
    baseUrl = "http://127.0.0.1:8000"

    async getHello(): Promise<PromptResponse> {
        try {
            const response = await fetch(`${this.baseUrl}/hello`);
            if (!response.ok) {
                throw new Error(`Request failed with status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error fetching places:", error);
            throw error;
        }
    }
}
