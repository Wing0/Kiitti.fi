from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.utils import *
import json


class TagAPI(APIView):

    def post(self, request):
        '''
        @params
            courseFlag: Determines whether tag is related to course or not.
            name: Name of tag.
        @example
            {
                "courseFlag": "false",
                "name": "Mathematics"
            }
        @returns
            201: If Tag was created successfully.
            400: If user input is invalid.
            401: If user is not logged in.
        '''
        messages = []
        data = json.loads(request.body)
        course_flag = string_to_boolean(data["courseFlag"])
        name = data["name"]
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request comments."), 401)
        if not isinstance(course_flag, bool):
            messages.append(compose_message("Course flag must be a boolean value.", "courseFlag"))
        if name == None or len(name) == 0:
            messages.append(compose_message("Name must be non-empty string.", "name"))
        if len(messages) == 0:
            tag = Tag(organization=request.user.organization, course_flag=course_flag, name=name)
            tag.user = request.user
            messages = tag.validate()
            if len(messages) == 0:
                tag.save()
                return Response(create_message("New tag was created successfully."), 201)

        return Response({"messages": messages}, 400)


    def get(self, request):

        '''
        This method mediates the task to correct function.
        Further information in helper method docstring
        '''
        if not request.user.is_authenticated():
            return Response({"messages":create_message("User must be logged in.")}, 401)
        else:
            if request.GET.get("tagId") != None:
                return self.by_id(request, request.GET.get("tagId"))
            elif request.GET.get("authorId") != None:
                return self.by_author(request, request.GET.get("authorId"), request.GET.get("limit"), request.GET.get("order"))
            else:
                return self.get_all(request, request.GET.get("limit"), request.GET.get("order"))

    def by_id(self, request, tag_id):
        '''
        Retrieves all tags, tags by id or by creator

        @params
            request: the request parameter from get function
            tagId, integer (optional): The ide of the tag to be retriveved.
        @example
            /tags/?tagId=123
        @perm
            member: All tag information can be given only for members of the organization.
        @return
            200:
                list of retrieved tags
                example: {
                            "tags":[{
                                        "courseFlag": false,
                                        "name": "exampletag",
                                        "created": "2014-02-02T00:00:00",
                                        "organizationId": 0,
                                        "tagId": 3,
                                        "creator": 1,
                                        "modified": "2014-02-02T00:00:00"
                                    }]
                        }
            404: No content found
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''
        messages = []
        if tag_id == None:
            messages.append({"content":"A tag id must be provided.","identifier":"tagId"})
        else:
            try:
                # Parameter check and default values
                tag_id = int(tag_id)
                if tag_id < 0:
                    raise ValueError("Value is not positive integer")

                try:
                    tag = Tag.objects.get(tag_id=tag_id)
                    if not tag.organization == request.user.organization:
                        messages.append(compose_message("You are not allowed to perform this action."))
                        return Response({"messages":messages}, 403)
                except:
                    messages.append({"content":"The tag was not found.","identifier":"tagId"})
                    return Response({"messages":messages}, 404)

                if len(messages) == 0:
                    return Response({"tags":tag.serialize(), "messages":messages}, 200)

            except ValueError:
                messages.append({"content":"The tag id has to be a positive integer.","identifier":"tagId"})
        return Response({"messages":messages}, 400)

    def by_author(self, request, author_id, limit=10, order="latest"):
        '''
        Retrieves tags written by user matching the authorId. Ordered and limited by given parameters

        @params
            request: the request parameter from get function
            authorId, integer (optional): The id of the tag author.
            limit, integer (optional): The maximum number of tags retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved tags. "popularity" or "latest". Default="latest".
        @example
            /tags/?authorId=123&limit=5&order=latest
        @perm
            member: All tag information can be given only for members of the organization.
        @return
            200:
                list of retrieved tags
                example: {
                            "tags":[{
                                        "courseFlag": false,
                                        "name": "exampletag",
                                        "created": "2014-02-02T00:00:00",
                                        "organizationId": 0,
                                        "tagId": 3,
                                        "creator": 1,
                                        "modified": "2014-02-02T00:00:00"
                                    },{...},{...}]
                        }
            404: No content found
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''
        messages = []
        try:
            author_id = int(author_id)
            if author_id < 0:
                raise ValueError("Value is not positive integer")

            if limit == None:
                limit = 10
            try:
                limit = int(limit)
                if limit < 0:
                    raise ValueError("Value is not positive integer")
            except ValueError:
                messages.append(compose_message("The limit has to be a positive integer.","limit"))

            if order == None:
                order = "latest"
            if not order in ["latest","popularity"]:
                messages.append(compose_message("The order parameter can be only 'latest' or 'popularity'","order"))

            try:
                author = User.objects.get(user_id = author_id)
            except:
                messages.append(compose_message("The user id does not match any user.", "userId"))

            if not request.user.organization == author.organization:
                messages.append(compose_message("You are not allowed to perform this action."))
                return Response({"messages":messages}, 403)

            if len(messages) == 0:
                if order == "latest":
                    tags = Tag.objects.filter(user = author).order_by("-created")[:limit]
                    tags = [tag.serialize() for tag in tags]
                else:
                    tags = Tag.objects.filter(user = author)
                    tags = [tag.serialize() for tag in tags]
                    tags.sort(key = lambda x: -x["count"])
                    tags = tags[:limit]

                return Response({"tags": tags, "messages":messages}, 200)

        except ValueError:
            messages.append({"content":"The author id has to be a positive integer.","identifier":"authorId"})

        return Response({"messages":messages}, 400)

    def get_all(self, request, limit=10, order="latest"):
        '''
        Retrieves all tags limited and ordered according to given parameters

        @params
            request: the request parameter from get function
            limit, integer (optional): The maximum number of tags retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved tags. "popularity" or "latest". Default="latest".
        @example
            /tags/?limit=5&order=latest
        @perm
            member: All tag information can be given only for members of the organization.
        @return
            200:
                list of retrieved tags
                example: {
                            "tags":[{
                                        "courseFlag": false,
                                        "name": "exampletag",
                                        "created": "2014-02-02T00:00:00",
                                        "organizationId": 0,
                                        "tagId": 3,
                                        "creator": 1,
                                        "modified": "2014-02-02T00:00:00"
                                    },{...},{...}]
                        }
            404: No content found
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''
        messages = []
        if limit == None:
            limit = 10
        try:
            limit = int(limit)
            if limit < 0:
                raise ValueError("Value is not positive integer")
        except ValueError:
            messages.append(compose_message("The limit has to be a positive integer.","limit"))

        if order == None:
            order = "latest"
        if not order in ["latest","popularity"]:
            messages.append(compose_message("The order parameter can be only 'latest' or 'popularity'","order"))

        if len(messages) == 0:
            if order == "latest":
                tags = Tag.objects.filter(organization = request.user.organization).order_by("-created")[:limit]
                tags = [tag.serialize() for tag in tags]
            else:
                tags = Tag.objects.filter(organization = request.user.organization)
                tags = [tag.serialize() for tag in tags]
                tags.sort(key= lambda x: -x["count"])
                tags = tags[:limit]

            return Response({"tags": tags, "messages":messages}, 200)

        return Response({"messages":messages}, 400)
