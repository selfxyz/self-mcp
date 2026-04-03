export declare function formatSuccess(data: unknown): {
    content: Array<{
        type: "text";
        text: string;
    }>;
};
export declare function formatError(message: string): {
    content: Array<{
        type: "text";
        text: string;
    }>;
    isError: true;
};
export declare function formatResource(content: string): string;
//# sourceMappingURL=format.d.ts.map