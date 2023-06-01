import axios from 'axios'
const elasticUrl = 'http://localhost:9200/documents-pages/_search'

export async function find(req, res) {
 const {terms} = req.body
 const query = createQuery(terms)
 const result = await searchElastic(query)
 res.json({result, ...query})
}

async function searchElastic(query) {
  return await axios.get(elasticUrl, query)
    .then((response) => {
        //todo: terminar esse tratamento
        return response.data
    })


}

function createQuery(terms){
  const shoulds = []
  terms.forEach(term => {
    shoulds.push({match_phrase:{content: term}})
  });
  return  {
    query: { 
      bool : {
          should: shoulds
        } 
    },
    fields: [
      "file-name",
      "file-path",
      "page-number"
    ],
    _source: false
  }
}