import express from 'express'
import bodyParser from 'body-parser'
import cors from 'cors'
import dotenv  from "dotenv"
import routes from './routes'
import {createErrorNotFound, errorHandler} from './configs'

dotenv.config()

const app = express()

app.use(cors())
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use('/', routes)


app.use(createErrorNotFound)
app.use(errorHandler);

// application Start
app.listen(process.env.PORT || 8000, () => {
    console.log(('App is running at %s:%d in %s mode'), process.env.HOST || 'http//localhost', process.env.PORT || 8000, app.get('env'))
    console.log('Press CTRL-C to stop\n')

});