import express, { application } from 'express'

const routes = express.Router()
const applicationContext = '/api/v1'

import { find } from '../controllers/elasticController'

routes.get(`${applicationContext}/server/info`, (req, res) => res.json({
  status: 'running...',
  timestamp: new Date()
}))

routes.get('/' , (req, res) => res.redirect(`${applicationContext}/server/info`))
routes.post(`${applicationContext}/find`, find )

export default routes