import datetime
import os

from disnake import Color, Embed

from src.sql.sql_manager import DBConnect
from src.dayz.clean_trader_file import open_config, parse_config


class TraderConfigManager(DBConnect):
    def load_traderconfig_to_db(self, map_name):
        items = parse_config(open_config(map_name))
        print(map_name)
        for idx, line in enumerate(items):
            self.insert_into_traderconfig(map_name, line[0], line[1], line[2], line[3], line[4], line[5])

            if idx % 25 == 0:
                print(f"{round((idx / len(items)) * 100, 2)}%")
                self.commit()
        self.commit()
        self.close()

    async def create_new_traderconfig(self, message, map_name):
        label = """
                  //---------------------------------------------------------------------------------------------//
                 //                                                                                             //
                //                                  generated on: {:<45}//
               //                             number of vendors: {:<45}//
              //                         total number of items: {:<45}//
             //                                                                                             //
            //---------------------------------------------------------------------------------------------//


    <CurrencyName> #tm_ruble
        <Currency> MoneyRuble1, 	1
        <Currency> MoneyRuble5, 	5
        <Currency> MoneyRuble10, 	10
        <Currency> MoneyRuble25, 	25
        <Currency> MoneyRuble50, 	50
        <Currency> MoneyRuble100, 	100


"""

        with open(f"_files/outputs/{map_name}/TraderConfig.txt", "w") as fout:
            stats = self.c.callproc("select_stats", args=(map_name, "", ""))
            today = datetime.date.today().strftime("%m/%d/%Y")
            start_time = datetime.datetime.now()

            fout.writelines(label.format(today, stats[1], stats[0]))


            self.c.callproc("select_map_traders", args=(map_name, ))
            traders_generator = self.c.stored_results()
            idx = 0
            
            for trader_c in traders_generator:
                trader_list = [i[0] for i in trader_c.fetchall()]


            est_perc = f"0.0%"  # embed
            for trader in trader_list:
                embed = Embed(title="Rendering TraderConfig.txt", description="This will a little bit of time", color=Color.yellow(), timestamp=start_time)
                embed.add_field(name=map_name, value=est_perc, inline=False)  # embed

                fout.write(f"<Trader> {trader}\n")
                self.c.callproc("select_map_trader_categories", args=(map_name, trader))
                category_generator = self.c.stored_results()

                for category_c in category_generator:
                    category_list = [i[0] for i in category_c.fetchall()]


                for category in category_list:

                    fout.write(f"\t<Category> {category}\n")
                    self.c.callproc("select_map_trader_category_products", args=(map_name, trader, category))
                    product_generator = self.c.stored_results()
                    
                    for product_c in product_generator:
                        product_list = product_c.fetchall()

                    embed.add_field(name=category, value=len(product_list), inline=True)  # embed
                    for product in product_list:
                        idx += 1
                        est_perc = f"{round((idx / stats[2]) * 100, 2)}%"

                        product_str = "\t\t{:<55}{:<5}{:<10}{:<10}\n"
                        fout.write(product_str.format(
                            str(product[0]) + ",", 
                            str(product[1]) + ",", 
                            str(product[2]) + ",", 
                            product[3]))
                    
                    fout.write("\n")
            fout.write("<FileEnd>")
            await message.edit(embed=embed)
            
            end_time = datetime.datetime.now()

            deltatime = end_time - start_time
            seconds_in_day = 24 * 60 * 60
            ex_time = divmod(deltatime.days * seconds_in_day + deltatime.seconds, 60)

            embed = Embed(title="Rendering TraderConfig.txt", description=f"This took {ex_time[0]} minutes and {ex_time[1]} seconds", color=Color.green(), timestamp=start_time)
            embed.add_field(name=map_name, value="Complete!", inline=True)
            embed.add_field(name="Items in file", value=stats[1], inline=True)

            await message.edit(embed=embed)


if __name__ == "__main__":
    tcm = TraderConfigManager()
    tcm.create_new_traderconfig("Namalsk")
    print("TraderConfig.txt Complete!")
