import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useCommentStore = defineStore('comment', () => {
    const comments = ref([])

    async function fetchComments(postId) {
        try {
            const res = await axios.get(`/api/community/comments/?post=${postId}`)
            comments.value = res.data
        } catch (err) {
            console.error('댓글 불러오기 실패:', err)
        }
    }

    async function createComment(postId, content) {
        const token = localStorage.getItem('authToken')
        try {
            await axios.post('/api/community/comments/', {
                post: postId,
                content
            }, {
                headers: { Authorization: `Token ${token}` }
            })
            await fetchComments(postId)
        } catch (err) {
            console.error('댓글 작성 실패:', err)
        }
    }

    async function deleteComment(postId, commentId) {
        const token = localStorage.getItem('authToken')
        try {
            await axios.delete(`/api/community/comments/${commentId}/`, {
                headers: { Authorization: `Token ${token}` }
            })
            await fetchComments(postId)
        } catch (err) {
            console.error('댓글 삭제 실패:', err)
        }
    }
    async function createComment(postId, content, parentId = null) {
        const token = localStorage.getItem('authToken')
        try {
            await axios.post('/api/community/comments/', {
                post: postId,
                content,
                parent: parentId,
            }, {
                headers: { Authorization: `Token ${token}` }
            })
            await fetchComments(postId)
        } catch (err) {
            console.error('댓글 작성 실패:', err)
        }
    }
    return {
        comments,
        fetchComments,
        createComment,
        deleteComment
    }
})
