import http from './http-common';

class AppRoutes {

    sendText(data: any) {
        return http.post(`/operations/process`, data);
    }

    execCode(data: any) {
        return http.post(`/operations/execute`, data);
    }

    undoCode() {
        return http.post(`/operations/undo`);
    }
}

export default new AppRoutes();