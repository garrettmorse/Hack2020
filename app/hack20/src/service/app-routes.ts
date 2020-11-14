import http from './http-common';

class AppRoutes {

    sendText(data: any) {
        return http.post(`/text`, data);
    }

    sendCode(data: any) {
        return http.post(`/code`, data);
    }
}

export default new AppRoutes();