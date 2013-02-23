static int authorizedtypes[] = { 1, 2, 4, 17, 18, 20, 36, 132, 148, -1 };

int checktype(int type)
{
    int i = 0;
    int t;
    while (t = authorizedtypes[i]) {
        if (t == type)
            return 1;
        i++;
    }
    return 0;
}
