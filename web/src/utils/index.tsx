import { useMantineColorScheme } from "@mantine/core";
import * as Icon from "react-feather";

const themePick = (dark: any, light: any) => {
  const { colorScheme } = useMantineColorScheme();
  return colorScheme === "dark" ? dark : light;
};

export { themePick, Icon };
