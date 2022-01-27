# Starting the app

* To start the app in a Docker container, from your machine, run bin/docker_build.bash. The script will call bin/run.sh from the container.

* To start the app from the container (or possibly any suitable environment although that is untested), run the bin/run.sh file.
The app.db database file will be recreated if it doesn't exist.

* To check the coverage, run bin/coverage.sh: it will run the tests and open them in your default browser

# Design

* The approach taken is that the root path is a "mind-map creator". It's technically not part of any mind map and thus acts specially. A mind map is actually a direct leaf to the root.
* The root node answers in plain text to GET requests (for pretty-printing, per Specification)
* Everything else answers strictly in JSON

# Interface

GET /
	Response 200
		Content-Type: text/plain
		Body:
			The plain text list of mind map root nodes
GET /?tree
	Response 200
		Content-Type: text/plain
		Body:
			The plain text pretty-printed mind map trees

GET /{mind-map-root-node}/{node1}/{node2}/{nodeN}
	Response 200
		Content-Type: application/json
		Body:
			"path": string
				{mind-map-root-node}/{node1}/{node2}/{nodeN}
			"text": string
				the display string for the node

	Response 404
		Content-Type: application/json
		Body:
			"message": string
				An explicative message why the request failed

POST /
	Request application/json
		"slug": string
			the root node's ID (also URL part)
		"id": string
			an alternative name for slug
		"text": The text to display for the node
	Response 200
		Content-Type: application/json
		Body:
			"message": string
				A message explaining that the node has been created or updated if it already existed

POST /{mind-map-nodeN}...
	Request application/json
		"slug": string
			the root node's ID (also URL part)
		"id": string
			an alternative name for slug
		"text": The text to display for the node
	Response 200
		Content-Type: application/json
		Body:
			"message": string
				A message explaining that the node has been created, or updated if it already existed
