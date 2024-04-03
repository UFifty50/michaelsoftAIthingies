import { DockviewReact, DockviewReadyEvent, IDockviewPanelProps } from "dockview";
import { useEffect, useState } from "react";
import * as React from "react";
import { Server, PromptResponse, FileUploadResponse } from "./server";


const Chatbot = () => {

    const [messages, setMessages] = useState([
        { text: 'Hello! How can I assist you today?', sender: 'bot' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [fileList, setFileList] = useState<string[]>([]);

    const handleMessageSubmit = () => {
        if (inputValue.trim() === '') return;
        setMessages(prevMessages => ([
            ...prevMessages,
            { text: inputValue, sender: 'user' }
        ]));

        handleFileUpload();

        console.log(JSON.stringify({ 'prompt': inputValue }));

        fetch('http://localhost:8000/api/v1/prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'prompt': inputValue })
        })
            .then(response => response.json())
            .then(data => {
                setMessages(prevMessages => ([
                    ...prevMessages,
                    { text: data.final, sender: 'bot' }
                ]));
            })
            .catch(error => {
                console.error('Error:', error);
            });

    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (!event.target.files) return;

        setSelectedFiles(Array.from(event.target.files));
        setFileList(Array.from(event.target.files).map(file => file.name));
    };


    const handleFileUpload = () => {
        if (selectedFiles.length === 0) return;

        const formData = new FormData();
        selectedFiles.forEach((file, index) => {
            formData.append(`files`, file);
        });

        fetch('http://localhost:8000/api/v1/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .catch(error => {
                console.error('Error:', error);
            });
    };

    return (
        <div className="chatbot-container">
            <div className="messages-container">
                {messages.map((message, index) => (
                    <div
                        key={message.sender + index}
                        className={`message ${message.sender}`}
                    >
                        {message.text}
                    </div>
                ))}
            </div>
            <input
                type="text"
                className="input-field"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                        handleMessageSubmit();
                    }
                }}
            />
            {/* <input
                type="file" id="selectFile" className="input-file" />
            <input type="button" value="Upload File" onClick={() => document.getElementById('selectFile')?.click()} className="upload-file" /> */}
            <button className="send-button" onClick={handleMessageSubmit}>Send</button>
            <div>
                <input className="upload-file" type="file" accept="text/csv, application/vnd.ms-excel" multiple onChange={handleFileChange} />
                <ul>
                    {fileList.map((fileName, index) => (
                        <li key={fileName + index}>{fileName}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};



const components = {
    dataViewer: (props: IDockviewPanelProps<{ title: string }>) => {
        return <div style={{ padding: 10 }}>{props.params.title}</div>;
    },

    graphViewer: (props: IDockviewPanelProps<{ title: string }>) => {
        return <div style={{ padding: 10 }}>{props.params.title}</div>;
    },

    taskViewer: (props: IDockviewPanelProps<{ title: string }>) => {
        return <div style={{ padding: 10 }}>{props.params.title}</div>;
    },

    chatViewer: (props: IDockviewPanelProps<{ title: string }>) => {
        return <Chatbot />;
    }
};

const App: React.FC = (props: { theme?: string }) => {
    const onReady = (event: DockviewReadyEvent) => {
        event.api.addPanel({
            id: "Data",
            component: "dataViewer",
            params: {
                //       title: "Hello World",
            },
        });

        event.api.addPanel({
            id: "Graph",
            component: "graphViewer",
            params: {
                //         title: "Graph",
            },
            position: { referencePanel: 'Data', direction: 'right' }
        });

        event.api.addPanel({
            id: "Task",
            component: "taskViewer",
            params: {
                //         title: "Task",
            },
            position: { referencePanel: 'Graph', direction: 'right' }
        });

        event.api.addPanel({
            id: "Chat",
            component: "chatViewer",
            params: {
                //         title: "Chat",
            },
            position: { referencePanel: 'Task', direction: 'below' }
        });
    };

    return <DockviewReact components={components} onReady={onReady} className={`${props.theme || 'dockview-theme-abyss'}`} />;
}


const Container = (props: any) => {
    return (
        <div className="app">
            <App {...props} />
        </div>
    );
}

export default Container;
