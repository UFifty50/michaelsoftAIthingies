import { DockviewReact, DockviewReadyEvent, IDockviewPanelProps } from "dockview";
import * as React from "react";

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
        return <div style={{ padding: 10 }}>{props.params.title}</div>;
    }
};

export const App: React.FC = (props: { theme?: string }) => {
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
            position: {referencePanel: 'Data', direction: 'right'}
        });

        event.api.addPanel({
            id: "Task",
            component: "taskViewer",
            params: {
       //         title: "Task",
            },
            position: {referencePanel: 'Graph', direction: 'right'}
        });

        event.api.addPanel({
            id: "Chat",
            component: "chatViewer",
            params: {
       //         title: "Chat",
            },
            position: {referencePanel: 'Task', direction: 'below'}
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
