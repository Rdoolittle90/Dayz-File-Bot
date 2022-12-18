import datetime
import os
from lxml.etree import _Element, _Comment, _ElementTree
from lxml.etree import parse

from src.sql.sql_manager import DBConnect

from lxml.etree import Element, ElementTree, indent, Comment

from disnake import Embed, Color



class XMLManager(DBConnect):

    def get_tree(self, xml) -> tuple:
        tree: _ElementTree = parse(xml)
        root: _Element = tree.getroot()
        return (tree, root)


    def refresh_xml_format(self, duid, map_name, xml_file):
        tree, root = self.get_tree(f"_files/{duid}/maps/{map_name}/inputs/{xml_file}")
        indent(tree, space="\t", level=0)
        tree.write(f'_files/{duid}/maps/{map_name}/inputs/{xml_file}', xml_declaration=True, encoding="utf-8", standalone=True)


    async def load_types_xml_to_db(self, message, duid, map_name: str, modal:int=35) -> None:
        for xml_file in os.listdir(f"_files/{duid}/maps/{map_name}/inputs"):
            if xml_file.endswith(".xml"):
                # clean the xml to matching format
                self.refresh_xml_format(duid, map_name, xml_file)

                tree, root = self.get_tree(f"_files/{duid}/maps/{map_name}/inputs/{xml_file}")
                root: _Element
                item_count = float(len(root))
                items_added = 0.0
                for idx, item in enumerate(root):
                    items_added += 1             
                    if idx % modal == 0:     
                        self.commit()   
        
                        est_perc = f"{round((idx / item_count) * 100, 2)}%"
                        embed = Embed(title=f"{map_name}", description=f"loading {xml_file} to db", color=Color.yellow())
                        embed.add_field(name=f"{idx}/{item_count}", value=est_perc)
                        await message.edit(embed=embed)
                        
                    if type(item) == _Comment:
                        pass
                    else:
                        item: _Element
                        item_list: list = [duid, map_name]

                        class_name = item.attrib["name"]

                        class_category: _Element = item.find("category")
                        class_nominal: _Element = item.find("nominal")
                        class_lifetime: _Element = item.find("lifetime")
                        class_restock: _Element = item.find("restock")
                        class_min: _Element = item.find("min")
                        class_quantmin: _Element = item.find("quantmin")
                        class_quantmax: _Element = item.find("quantmax")
                        class_cost: _Element = item.find("cost")
                        class_flags: _Element = item.find("flags")

                        # check to see if the above elements are None
                        if class_category != None:
                            class_category = class_category.attrib["name"]
                        else:
                            class_category = "uncategorized"

                        if class_nominal != None:
                            class_nominal = class_nominal.text
                        else:
                            class_nominal = 0

                        if class_lifetime != None:
                            class_lifetime = class_lifetime.text

                        if class_restock != None:
                            class_restock = class_restock.text
                        else:
                            class_restock = 2700

                        if class_min != None:
                            class_min = class_min.text
                        else:
                            class_min = 0

                        if class_quantmin != None:
                            class_quantmin = class_quantmin.text
                        else:
                            class_quantmin = -1

                        if class_quantmax != None:
                            class_quantmax = class_quantmax.text
                        else:
                            class_quantmax = -1

                        if class_cost != None:
                            class_cost = class_cost.text

                        if class_flags != None:
                            class_flags = class_flags.attrib.values()


                        class_tier = None
                        tiers = []
                        for value in item.findall("value"):
                            value: _Element
                            if value == None:
                                continue
                            if len(value.attrib.values()) != 0:
                                tiers.append(value.attrib.values()[0].strip("Tier"))
                        if len(tiers) > 0:
                            class_tier = "Tier" + "".join(tiers)


                        class_usage = None
                        usage = []

                        for value in item.findall("usage"):
                            value: _Element
                            if value == None:
                                continue
                            if len(value.attrib.values()) != 0:
                                usage.append(value.attrib.values()[0])
                                usage.sort()
                        if len(usage) > 0:
                            class_usage = "".join(usage)


                        class_tag = None
                        tags = []
                        for value in item.findall("tag"):
                            value: _Element
                            if value == None:
                                continue
                            if len(value.attrib.values()) != 0:
                                tags.append(value.attrib.values()[0])
                                tags.sort()
                        if len(tags) > 0:
                            class_tag = ",".join(tags)

                        # item_list already contains the mapname append the remaining values
                        item_list.append(class_name)
                        item_list.append(class_category)
                        item_list.append(class_nominal)
                        item_list.append(class_lifetime)
                        item_list.append(class_restock)
                        item_list.append(class_min)
                        item_list.append(class_quantmin)
                        item_list.append(class_quantmax)
                        item_list.append(class_cost)
                        item_list.append(class_tier)
                        item_list.append(class_usage)
                        item_list.append(class_tag)
                        # class_flags is a list of boolean values append this list to the end
                        item_list += class_flags

                        # append these values again for the sake of updating
                        item_list.append(class_category)
                        item_list.append(class_nominal)
                        item_list.append(class_min)
                        item_list.append(class_cost)

                        # print(class_name)
                        # print(class_tier)
                        # print(class_usage)
                        # print(class_tag)

                        # insert item_list into typestable table 
                        self.insert_into_typestable(item_list)

                self.commit()
        self.close()


    async def create_new_types(self, message, duid, map_name) -> None:
        """get all items from db and convert them to xml objects"""
        root_types: _Element = Element("types")
        tree: _ElementTree = ElementTree(root_types)

        self.select_all_from_typestable(duid, map_name)
        rows = self.c.fetchall()
        column_names = self.c.column_names
        print(column_names)
        item_count = len(rows)
        items_added = 0

        start_time = datetime.datetime.now()

        ## before starting add file info comment
        comment_map = Comment(f"Map Name: {map_name}")
        comment_time = Comment(f"Created on: {start_time}")
        comment_items = Comment(f"Item Count: {len(rows)}")

        root_types.append(comment_map)
        root_types.append(comment_time)
        root_types.append(comment_items)

        ## start the loop over rows
        for idx, row in enumerate(rows):
            items_added += 1             
            if idx % 35 == 0:
                est_perc = f"{round((items_added / item_count) * 100, 2)}%"

                embed = Embed(title="Rendering types.xml", description="This will take some time.", color=Color.yellow(), timestamp=start_time)
                embed.add_field(name=map_name, value=est_perc)

                await message.edit(embed=embed)


            type_name:_Element = Element("type", attrib={"name": row[2]})

            category:_Element = Element("category", attrib={"name": row[3]})
            type_name.append(category)

            nominal:_Element = Element("nominal")
            nominal.text = str(row[4])
            type_name.append(nominal)

            lifetime:_Element = Element("lifetime")
            lifetime.text = str(row[5])
            type_name.append(lifetime)

            restock:_Element = Element("restock")
            restock.text = str(row[6])
            type_name.append(restock)

            min:_Element = Element("min")
            min.text = str(row[7])
            type_name.append(min)

            quantmin:_Element = Element("quantmin")
            quantmin.text = str(row[8])
            type_name.append(quantmin)

            quantmax:_Element = Element("quantmax")
            quantmax.text = str(row[9])
            type_name.append(quantmax)

            cost:_Element = Element("cost")
            cost.text = str(row[10])
            type_name.append(cost)


            if row[11] is not None:
                type_name.append(Element("value", attrib={"user":  row[11]}))

            if row[12] is not None and map_name == "Chernarus":
                values = row[12].split(",")
                for value in values:
                    type_name.append(Element("usage", attrib={"user": value}))
            
            if row[13] is not None:
                tags = row[13].split(",")
                for tag in tags:
                    type_name.append(Element("tag", attrib={"name": tag}))


            # flags is the only tag with multiple attributes and was normalized in the db this recreates the dict 
            type_name.append(
                Element("flags", attrib={
                    "count_in_map": str(row[14]), 
                    "count_in_hoarder": str(row[15]), 
                    "count_in_cargo": str(row[16]),
                    "count_in_player": str(row[17]), 
                    "crafted": str(row[18]),
                    "deloot": str(row[19])
                    }
                )
            )
            root_types.append(type_name)


        # format the output to be more readable
        indent(tree, space="\t", level=0)

        end_time = datetime.datetime.now()

        deltatime = end_time - start_time
        seconds_in_day = 24 * 60 * 60
        ex_time = divmod(deltatime.days * seconds_in_day + deltatime.seconds, 60)

        embed = Embed(title="Rendering types.xml", description=f"This took {ex_time[0]} minutes and {ex_time[1]} seconds", color=Color.green(), timestamp=start_time)
        embed.add_field(name=map_name, value="Complete!", inline=True)
        embed.add_field(name="Items in file", value=item_count, inline=True)

        await message.edit(embed=embed)

        tree.write(f'_files/{duid}/maps/{map_name}/outputs/types.xml', xml_declaration=True, encoding="utf-8", standalone=True)

