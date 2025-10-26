/**
 * API Service
 * Handles all API requests to the backend
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for resume analysis
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})

/**
 * Analyze resume file
 * @param {File} file - Resume file (PDF or DOCX)
 * @param {string} jobUrl - Optional job posting URL for comparison
 * @returns {Promise<Object>} Analysis result
 */
export const analyzeResume = async (file, jobUrl = '') => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    if (jobUrl && jobUrl.trim()) {
      formData.append('job_url', jobUrl.trim())
    }

    const response = await api.post('/analyze', formData, {
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        console.log(`Upload progress: ${percentCompleted}%`)
      },
    })

    if (response.data.success) {
      return response.data.data
    } else {
      throw new Error(response.data.error?.message || 'Analysis failed')
    }
  } catch (error) {
    console.error('API Error:', error)

    if (error.response) {
      // Server responded with error
      const errorData = error.response.data
      throw new Error(
        errorData.error?.message || 'Server error occurred'
      )
    } else if (error.request) {
      // Request made but no response
      throw new Error(
        'No response from server. Please check your connection.'
      )
    } else {
      // Error setting up request
      throw new Error(error.message || 'An unexpected error occurred')
    }
  }
}

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

/**
 * Get skill categories
 * @returns {Promise<Array>} List of skill categories
 */
export const getSkillCategories = async () => {
  try {
    const response = await api.get('/skills/categories')
    if (response.data.success) {
      return response.data.categories
    }
    return []
  } catch (error) {
    console.error('Failed to fetch skill categories:', error)
    return []
  }
}

export default api
