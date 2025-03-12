import axios from 'axios';

const API_BASE_URL = 'http://192.168.1.27:8000';

const userService = {
    getUsers: async (skip: number = 0, limit: number = 100) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/users/?skip=${skip}&limit=${limit}`);
            return response.data;
        } catch (error) {
            console.error("Error fetching users:", error);
            throw error;
        }
    },

    createUser: async (userData: any) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/users/`, userData);
            return response.data;
        } catch (error) {
            console.error("Error creating user:", error);
            throw error;
        }
    },

    getUser: async (userId: number) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/users/${userId}`);
            return response.data;
        } catch (error) {
            console.error("Error fetching user:", error);
            throw error;
        }
    },

    updateUser: async (userId: number, userData: any) => {
        try {
            const response = await axios.put(`${API_BASE_URL}/users/${userId}`, userData);
            return response.data;
        } catch (error) {
            console.error("Error updating user:", error);
            throw error;
        }
    },

    deleteUser: async (userId: number) => {
        try {
            await axios.delete(`${API_BASE_URL}/users/${userId}`);
        } catch (error) {
            console.error("Error deleting user:", error);
            throw error;
        }
    }
};

export default userService;
